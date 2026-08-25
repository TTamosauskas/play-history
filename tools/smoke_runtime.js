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
        if (event.immediateStopped) break;
      }
      return !event.defaultPrevented;
    },
    setAttribute() {}, removeAttribute() {}, replaceChildren() {},
    appendChild() {}, focus() {}, blur() {},
    close() { target.open = false; }, showModal() { target.open = true; },
    scrollTo() {}, querySelectorAll() { return []; }, querySelector() { return null; },
    closest() { return null; },
    getBoundingClientRect() { return { width: 100, height: 100 }; },
    innerHTML: '', textContent: '', title: '', href: '', src: '', alt: '', open: false,
    async: true, onload: null, onerror: null,
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
    this.immediateStopped = false;
  }
  preventDefault() { if (this.cancelable) this.defaultPrevented = true; }
  stopImmediatePropagation() { this.immediateStopped = true; }
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

  const files = new Map([
    ['./assets/catalog.json', fs.readFileSync(path.join(SITE, 'assets/catalog.json'), 'utf8')],
    ['./assets/js/app.js', fs.readFileSync(path.join(SITE, 'assets/js/app.js'), 'utf8')],
    ['./assets/js/services.js', fs.readFileSync(path.join(SITE, 'assets/js/services.js'), 'utf8')],
    ['./assets/js/player.js', fs.readFileSync(path.join(SITE, 'assets/js/player.js'), 'utf8')],
    ['./assets/js/bootstrap.js', fs.readFileSync(path.join(SITE, 'assets/js/bootstrap.js'), 'utf8')]
  ]);

  function cleanUrl(url) {
    return String(url).replace(/[?&]v=[^&]+/, '').replace(/\?$/, '');
  }

  head.appendChild = node => {
    if (node.text) throw new Error('Inline runtime injection is forbidden by this smoke test');
    if (!node.src) return node;
    const key = cleanUrl(node.src);
    if (!files.has(key)) {
      queueMicrotask(() => node.onerror?.(new Error(`missing ${key}`)));
      return node;
    }
    vm.runInContext(files.get(key), context, { filename: key });
    queueMicrotask(() => node.onload?.());
    return node;
  };

  context.fetch = async url => {
    await new Promise(resolve => setTimeout(resolve, 25));
    const key = cleanUrl(url);
    if (!files.has(key)) return { ok: false, status: 404, text: async () => '', json: async () => ({}) };
    const body = files.get(key);
    return { ok: true, status: 200, text: async () => body, json: async () => JSON.parse(body) };
  };

  const loaderSource = fs.readFileSync(path.join(SITE, 'assets/loader.js'), 'utf8');
  assert.ok(loaderSource.includes("script.src = versionedUrl(url)"), 'o loader deve usar scripts externos nativos');
  assert.ok(loaderSource.includes("window.selectYear"), 'o entry point deve chamar selectYear diretamente');
  assert.ok(loaderSource.includes("handleYearEntryInput"), 'o entry point deve possuir o listener permanente de input');
  assert.ok(!loaderSource.includes('script.text ='), 'o loader não deve reinjetar módulos como JavaScript inline');
  const loaderPromise = vm.runInContext(loaderSource, context, { filename: 'loader.js' });

  const yearInput = get('yearInput');
  const yearForm = get('yearForm');
  yearInput.value = '1953';
  yearInput.dispatchEvent(new MockEvent('input', { bubbles: true, cancelable: true }));

  await loaderPromise;
  await new Promise(resolve => setTimeout(resolve, 20));

  assert.ok(yearForm._listeners.get('submit')?.length, 'yearForm precisa ter listener de submit após o bootstrap');
  assert.ok(yearInput._listeners.get('input')?.length, 'yearInput precisa ter listener de input após o bootstrap');
  assert.strictEqual(String(yearInput.value), '1953', 'o ano digitado durante o carregamento deve ser preservado');
  assert.strictEqual(yearInput.dataset.resolvedYear, '1953', 'o ano digitado durante o carregamento deve ser executado após o bootstrap');
  assert.strictEqual(playerCard.hidden, false, 'a seleção por ano deve abrir o player');
  assert.notStrictEqual(get('trackTitle').textContent, 'Escolha um ano', 'a seleção por ano deve renderizar uma faixa');
  assert.ok(!app.classList.contains('is-start-screen'), 'a tela inicial deve sair do estado inicial após a seleção');

  // Exact user gesture: type a year after bootstrap and do nothing else.
  yearInput.value = '1969';
  yearInput.dispatchEvent(new MockEvent('input', { bubbles: true, cancelable: true }));
  await new Promise(resolve => setTimeout(resolve, 220));
  assert.strictEqual(yearInput.dataset.resolvedYear, '1969', 'digitar o ano deve resolver automaticamente sem Enter');
  assert.strictEqual(get('trackTitle').textContent, 'Come Together', '1969 digitado deve selecionar a faixa esperada');

  // Enter remains an immediate fallback.
  yearInput.value = '1970';
  yearForm.dispatchEvent(new MockEvent('submit', { bubbles: true, cancelable: true }));
  assert.strictEqual(yearInput.dataset.resolvedYear, '1970', 'Enter deve continuar selecionando imediatamente');

  console.log(`OK: digitação direta por ano -> ${get('trackTitle').textContent} (${yearInput.dataset.resolvedYear})`);
}

main().catch(error => {
  console.error(error);
  process.exit(1);
});
