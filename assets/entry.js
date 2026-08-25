/* Play History v6.8.0 — stable year-entry controller. */
(() => {
  const MIN_YEAR = 800;
  const MAX_YEAR = 2026;
  let selector = null;
  let ready = false;
  let timer = null;
  let pendingYear = "";
  let input = null;
  let form = null;

  function value(){ return String(input?.value || "").trim(); }
  function valid(raw){
    const text = String(raw || "").trim();
    if (!/^\d{3,4}$/.test(text)) return false;
    const year = Number(text);
    return year >= MIN_YEAR && year <= MAX_YEAR;
  }
  function reportError(error){
    console.error("Falha ao selecionar ano", error);
    const status = document.getElementById("status");
    if (status) status.textContent = "Falha ao selecionar o ano. Recarregue a página.";
  }
  function apply(raw, autoplay = true){
    const text = String(raw || "").trim();
    pendingYear = text;
    if (!valid(text) || !ready || typeof selector !== "function") return false;
    try { return selector(Number(text), Boolean(autoplay)) !== false; }
    catch (error) { reportError(error); return false; }
  }
  function onInput(event){
    pendingYear = value();
    event?.stopImmediatePropagation?.();
    clearTimeout(timer);
    if (!valid(pendingYear)) return;
    const requested = pendingYear;
    timer = setTimeout(() => {
      if (requested === value()) apply(requested, true);
    }, 160);
  }
  function onSubmit(event){
    event?.preventDefault?.();
    event?.stopImmediatePropagation?.();
    clearTimeout(timer);
    pendingYear = value();
    apply(pendingYear, true);
  }
  function bind(){
    input = document.getElementById("yearInput");
    form = document.getElementById("yearForm");
    pendingYear = value();
    input?.addEventListener("input", onInput);
    input?.addEventListener("change", onInput);
    form?.addEventListener("submit", onSubmit);
  }
  function setReady(selectYearFn){
    selector = selectYearFn;
    ready = typeof selector === "function";
    document.documentElement.dataset.playerReady = ready ? "true" : "false";
    const raw = pendingYear || value();
    if (ready && valid(raw)) queueMicrotask(() => apply(raw, true));
  }

  window.PlayHistoryEntry = { setReady, select: apply, isReady: () => ready };
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", bind, {once:true});
  else bind();
})();
