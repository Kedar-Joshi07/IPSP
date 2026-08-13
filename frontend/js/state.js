const state = {
  apiInfo: null,
  identity: null,
  flash: null,
};

export function getState() { return state; }
export function setApiInfo(value) { state.apiInfo = value; }
export function setIdentity(value) { state.identity = value; }
export function clearIdentity() { state.identity = null; }
export function setFlash(kind, message) { state.flash = { kind, message }; }
export function takeFlash() { const value = state.flash; state.flash = null; return value; }
