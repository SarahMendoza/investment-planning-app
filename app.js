
function login() {
  const username = document.getElementById('username').value;
  const password = document.getElementById('password').value;

  fetch('http://127.0.0.1:5000/user/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password })
  })
  .then(response => response.json())
  .then(data => {
    if (data.user_name) {
      localStorage.setItem('user_name', data.user_name);
      window.location.href = 'dashboard.html';
    } else {
      alert(data.message || 'Login failed');
    }
  })
  .catch(err => alert('Error: ' + err));
}

function goToCreateAccount() {
  window.location.href = 'create_account.html';
}
