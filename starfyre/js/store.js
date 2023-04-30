observers = {}; // uuid , list[observers]

const domIdMap = {};

function addDomIdToMap(domId, pyml) {
  domIdMap[domId] = pyml;
}

function getPymlFromDomId(domId) {
  return domIdMap[domId];
}

function render(domId) {
  const element = document.getElementById(domId);
  const pyml = getPymlFromDomId(domId);
  element.innerHTML = `${eval(pyml)}`;
}

function create_signal(initial_state) {
  let id = Math.random() * 1000000000000000; // simulating uuid
  let state = initial_state;

  function use_signal(domId) {
    if (!domId) {
      // when the domId is not provided, it means that the signal is used in a function component
      return store[id] || initial_state;
    }

    if (observers[id]) {
      observers[id].push(domId);
    } else {
      observers[id] = [domId];
    }

    return state;
  }

  function set_signal(newState) {
    state = newState;

    if (!observers[id]) {
      return;
    }

    observers[id].forEach((element) => {
      render(element);
    });
  }

  function get_signal() {
    return state;
  }

  return [use_signal, set_signal, get_signal];
}
