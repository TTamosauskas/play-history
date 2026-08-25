#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const vm = require('vm');
const assert = require('assert');

const ROOT = path.resolve(__dirname, '..');
const SITE = path.join(ROOT, '_site');

function makeElement(id = '') {
  const listeners = new Map();
  const classes = new Set(id === 'app' ? ['app', 'is-start-screen'] : []);
  const target = {
    id,
    hidden: id === 'playerCard',
    value: '',
    dataset: {},
    style: { setProperty() {}, removeProperty() {} },
    classList: {
      add(...names) { names.forEach(name => classes.add(name)); },
      remove(...names) { names.forEach(name => classes.delete(name)); },
      toggle(name, force) {
        if (force === undefined) force = !classes.has(name);
        if (force) classes.add(name); else classes.delete(name);
        return force;
      },
      contains(name) { return classes.has(name); }
    },
    addEventListener(type, fn) {
      if (!listeners.has(type)) listeners.set(type, []);
      listeners.get(type).push(fn);
    },
    removeEventListener(type, fn) {
      const current = listeners.get(type) || [];
      listeners.set(type, current.filter(item => item !== fn));
    },
    dispatchEvent(event) {
      event.target ||= target;
      for (const fn of [...(listeners.get(event.type) || [])]) {
        fn.call(target, event);
        if (event._immediateStopped) break;
      }
      return !event.defaultPrevented;
    },
    setAttribute(name, value) { target[name] = String(value); },
    removeAttribute(name) { delete target[name]; },
    replaceChildren() {}, appendChild() {}, focus() {}, blur() {},
    close() { target.open = false; }, showModal() { target.open = true; },
    scrollTo() {}, querySelectorAll() { return []; }, querySelector() { return null; },
    closest() { return null; },
    getBoundingClientRect() { return { width: 100, height: 100 }; },
    innerHTML: '', textContent: '', title: '', href: '', src: '', alt: '', open: false,
    scrollTop: 0, scrollHeight: 0, clientHeight: 0,
    _listeners: listeners
  };
  return target;
}

class MockEvent {
  constructor(type, options = {}) {
    this.type = type;
    this.bubbles = Boolean(options.bubbles);
    this.cancelable = Boolean(options.cancelable);
    this.defaultPrevented = false;
    this._immediateStopped = false;
  }
  preventDefault() { if (this.cancelable) this.defaultPrevented = true; }
  stopImmediatePropagation() { this._immediateStopped = true; }
}

async function main() {
  const elements = new Map();
  const get = id => {
    if (!elements.has(id)) elements.set(id, makeElement(id));
    return elements.get(id);
  };
  const app = get('app');
  const playerCard = get('playerCard');
  const document = {
    readyState: 'complete',
    getElementById: get,
    querySelector(selector) { return selector === '.player-card' ? playerCard : get(`qs:${selector}`); },
    createElement(tag) { return makeElement(tag); },
    head: get('head'), body: get('body'), documentElement: get('html'),
    activeElement: null, hidden: false,
    addEventListener() {}, removeEventListener() {}
  };
  document.head.appendChild = node => node;

  const context = {
    console, document,
    location: { search: '', protocol: 'https:', href: 'https://example.test/' },
    URLSearchParams, URL,
    setTimeout, clearTimeout, setInterval: () => 1, clearInterval,
    queueMicrotask,
    requestAnimationFrame: fn => { if (typeof fn === 'function') fn(); return 1; },
    cancelAnimationFrame() {}, performance: { now: () => 0 },
    matchMedia: () => ({ matches: false }), AbortController,
    localStorage: { getItem() { return null; }, setItem() {}, removeItem() {} },
    navigator: {}, Image: function Image() { return makeElement('img'); }, Event: MockEvent
  };
  context.addEventListener = () => {};
  context.removeEventListener = () => {};
  context.window = context;
  context.globalThis = context;
  vm.createContext(context);

  const scripts = [
    'assets/entry.js',
    'assets/catalog.js',
    'assets/js/app.js',
    'assets/js/services.js',
    'assets/js/player.js',
    'assets/js/bootstrap.js'
  ];
  for (const rel of scripts) {
    const source = fs.readFileSync(path.join(SITE, rel), 'utf8');
    vm.runInContext(source, context, { filename: rel });
  }

  assert.strictEqual(context.PLAY_HISTORY.catalog.length, 1726, 'catálogo deve carregar 1726 faixas');
  assert.strictEqual(context.PlayHistoryEntry.isReady(), true, 'controlador de ano deve ficar pronto após bootstrap');
  assert.strictEqual(get('html').dataset.playerReady, 'true', 'bootstrap deve sinalizar player pronto');

  const yearInput = get('yearInput');
  yearInput.value = '1969';
  yearInput.dispatchEvent(new MockEvent('input', { bubbles: true, cancelable: true }));
  await new Promise(resolve => setTimeout(resolve, 220));
  assert.strictEqual(yearInput.dataset.resolvedYear, '1969', 'digitar 1969 e esperar deve resolver o ano');
  assert.strictEqual(get('trackTitle').textContent, 'Come Together', '1969 deve selecionar Come Together');
  assert.strictEqual(playerCard.hidden, false, 'digitar um ano deve abrir o player');
  assert.ok(!app.classList.contains('is-start-screen'), 'a tela inicial deve desaparecer após a seleção');

  yearInput.value = '1953';
  yearInput.dispatchEvent(new MockEvent('input', { bubbles: true, cancelable: true }));
  await new Promise(resolve => setTimeout(resolve, 220));
  assert.strictEqual(yearInput.dataset.resolvedYear, '1953');
  assert.strictEqual(get('trackTitle').textContent, "That's Amore");

  assert.strictEqual(typeof context.YT, 'undefined', 'busca por ano deve funcionar antes da API do YouTube existir');
  console.log('OK: boot direto + digitar ano -> Come Together / That\'s Amore, sem YT disponível.');
}

main().catch(error => {
  console.error(error);
  process.exit(1);
});
