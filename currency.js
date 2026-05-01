const rates = {
  GBP: 3220,
  USD: 2560,
  EUR: 2780
};

function convert() {
  const amount = parseFloat(document.getElementById('amount').value);
  const currency = document.getElementById('currency').value;
  const resultBox = document.getElementById('result-box');
  const resultAmount = document.getElementById('result-amount');
  const resultRate = document.getElementById('result-rate');

  if (isNaN(amount) || amount <= 0) {
    alert('Please enter a valid amount.');
    return;
  }

  const rate = rates[currency];
  const result = (amount * rate).toLocaleString();

  resultAmount.textContent = result + ' SOS';
  resultRate.textContent = amount + ' ' + currency + ' x ' + rate.toLocaleString() + ' = ' + result + ' Somali Shillings';
  resultBox.style.display = 'block';
}

document.addEventListener('DOMContentLoaded', function() {
  document.getElementById('amount').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') convert();
  });
});