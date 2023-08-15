function copyResults() {
  const element = document.querySelector('#endScore');
  element.select();
  element.setSelectionRange(0, 99999);
  document.execCommand('copy');
}
