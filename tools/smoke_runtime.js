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
      for (const fn of [...(listeners.get(event.type) || [])]) fn.call(target, event);
      return !event.defaultPrevented;
    },
    setAttribute() {}, removeAttribute() {}, replaceChildren() {},
    appendChild() {}, focus() {}, blur() {},
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
  }
  preventDefault() { if (this.cancelable) this.defaultPrevented = true; }
}

async function main() {
  const elements = new Map();
  const get = id => {
    if (!elements.has(id)) elements.set(id, makeElement(id));
    return elements.get(id);
  };
  const app = get('app');
  const playerCard = get('playerCard');
  const head = get('head');
  const document = {
    getElementById: get,
    querySelector(selector) { return selector === '.player-card' ? playerCard : get(`qs:${selector}`); },
    createElement(tag) { return makeElement(tag); },
    head,
    body: get('body'),
    documentElement: get('html'),
    activeElement: null,
    hidden: false,
    addEventListener() {}, removeEventListener() {}
  };

  const context = {
    console,
    document,
    location: { search: '', protocol: 'https:', href: 'https://example.test/' },
    URLSearchParams, URL,
    setTimeout, clearTimeout, setInterval: () => 1, clearInterval,
    queueMicrotask,
    requestAnimationFrame: () => 0, cancelAnimationFrame() {},
    performance: { now: () => 0 },
    matchMedia: () => ({ matches: false }),
    AbortController,
    localStorage: { getItem() { return null; }, setItem() {}, removeItem() {} },
    navigator: {},
    Image: function Image() { return makeElement('img'); },
    Event: MockEvent,
    YT: { PlayerState: { PLAYING: 1, PAUSED: 2, CUED: 5, ENDED: 0 } }
  };
  context.addEventListener = () => {};
  context.removeEventListener = () => {};
  context.window = context;
  context.globalThis = context;
  vm.createContext(context);

  head.appendChild = node => {
    if (node.text) vm.runInContext(node.text, context, { filename: node.src || 'dynamic-script.js' });
    return node;
  };

  const files = new Map([
    ['./assets/catalog.json', fs.readFileSync(path.join(SITE, 'assets/catalog.json'), 'utf8')],
    ['./assets/js/app.js', fs.readFileSync(path.join(SITE, 'assets/js/app.js'), 'utf8')],
    ['./assets/js/services.js', fs.readFileSync(path.join(SITE, 'assets/js/services.js'), 'utf8')],
    ['./assets/js/player.js', fs.readFileSync(path.join(SITE, 'assets/js/player.js'), 'utf8')],
    ['./assets/js/bootstrap.js', fs.readFileSync(path.join(SITE, 'assets/js/bootstrap.js'), 'utf8')]
  ]);

  context.fetch = async url => {
    await new Promise(resolve => setTimeout(resolve, 25));
    const key = String(url).replace(/[?&]v=[^&]+/, '').replace(/\?$/, '');
    if (!files.has(key)) return { ok: false, status: 404, text: async () => '', json: async () => ({}) };
    const body = files.get(key);
    return { ok: true, status: 200, text: async () => body, json: async () => JSON.parse(body) };
  };

  const loaderSource = fs.readFileSync(path.join(SITE, 'assets/loader.js'), 'utf8');
  const loaderPromise = vm.runInContext(loaderSource, context, { filename: 'loader.js' });

  const yearInput = get('yearInput');
  const yearForm = get('yearForm');
  yearInput.value = '1953';
  yearInput.dispatchEvent(new MockEvent('input', { bubbles: true, cancelable: true }));

  await loaderPromise;
  await new Promise(resolve => setTimeout(resolve, 10));

  assert.ok(yearForm._listeners.get('submit')?.length, 'yearForm precisa ter listener de submit após o bootstrap');
  assert.ok(yearInput._listeners.get('input')?.length, 'yearInput precisa ter listener de input após o bootstrap');
  assert.strictEqual(String(yearInput.value), '1953', 'o ano digitado durante o carregamento deve ser preservado');
  assert.strictEqual(yearInput.dataset.resolvedYear, '1953', 'o ano digitado durante o carregamento deve ser executado após o bootstrap');
  assert.strictEqual(playerCard.hidden, false, 'a seleção por ano deve abrir o player');
  assert.notStrictEqual(get('trackTitle').textContent, 'Escolha um ano', 'a seleção por ano deve renderizar uma faixa');
  assert.ok(!app.classList.contains('is-start-screen'), 'a tela inicial deve sair do estado inicial após a seleção');

  const playerSource = files.get('./assets/js/player.js');
  assert.ok(playerSource.includes('/^\\d{3,4}$/.test(raw)'), 'a seleção automática deve aceitar anos de 800 a 999');

  console.log(`OK: busca inicial por ano -> ${get('trackTitle').textContent} (${yearInput.dataset.resolvedYear})`);
}

main().catch(error => {
  console.error(error);
  process.exit(1);
});
