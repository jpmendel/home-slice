function deleteElementById(id) {
  const element = document.getElementById(id);
  element.parentElement.removeChild(element);
}

function setCssById(id, style) {
  const element = document.getElementById(id);
  for (const [key, value] of Object.entries(style)) {
    element.style[key] = value;
  }
}

function colorFromHue(hue) {
  if (hue === 0) {
    return 'rgb(0, 0, 0)';
  } else if (hue === 255) {
    return 'rgb(255, 255, 255)';
  }
  const h = hue / 255;
  const kr = (5 + h * 6) % 6;
  const kg = (3 + h * 6) % 6;
  const kb = (1 + h * 6) % 6;

  const r = Math.round((1 - Math.max(Math.min(kr, 4 - kr, 1), 0)) * 255);
  const g = Math.round((1 - Math.max(Math.min(kg, 4 - kg, 1), 0)) * 255);
  const b = Math.round((1 - Math.max(Math.min(kb, 4 - kb, 1), 0)) * 255);
  return `rgb(${r}, ${g}, ${b})`;
}
