// Login

function login() {
  const my_username = document.getElementById("username").value;
  const my_password = document.getElementById("password").value;

  fetch("http://127.0.0.1:5000/user/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ user_name: my_username, password: my_password }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.user_name) {
        localStorage.setItem("user_name", data.user_name);
        window.location.href = "dashboard.html";
      } else {
        alert(data.message || "Login failed");
      }
    })
    .catch((err) => alert("Error: " + err));
}

function goToCreateAccount() {
  window.location.href = "create_account.html";
}

// Investments

function openStockModal() {
  document.getElementById('stockModal').style.display = 'flex';

  fetch('http://localhost:5000/api/stocks')  // Adjust this URL to match your backend
    .then(res => res.json())
    .then(data => {
      const container = document.getElementById('stockRows');
      container.innerHTML = ""; // Clear any previous content

      data.forEach(stock => {
        const row = document.createElement('div');
        row.className = "stock-row";
        row.innerHTML = `
          <span style="flex: 2;">${stock.name}</span>
          <span style="flex: 0.8;">${stock.risk}</span>
          <span style="flex: 0.8;">${stock.rate}</span>
          <span style="flex: 0.8; text-align: right;" class="eyeball" onclick="alert('Graph for ${stock.name}')">
            <i class="fas fa-eye"></i>
          </span>
        `;
        container.appendChild(row);
      });
    })
    .catch(err => {
      console.error("Failed to fetch stock data:", err);
    });

    function closeStockModal() {
      document.getElementById('stockModal').style.display = 'none';
    }

    window.onclick = function(event) {
      const modal = document.getElementById('stockModal');
      if (event.target === modal) {
        closeStockModal();
      }
    }

    function loadFixedAssets() {
      fetch('http://localhost:5000/api/fixed-assets') // Adjust to your real API
        .then(res => res.json())
        .then(data => {
          const container = document.getElementById('fixedAssetsContainer');
          container.innerHTML = ""; // Clear old entries
    
          data.forEach(asset => {
            const row = document.createElement('div');
            row.className = "labeled-row";
            row.innerHTML = `
              <span>${asset.label}</span>
              <strong>${asset.value}</strong>
            `;
            container.appendChild(row);
            container.appendChild(document.createElement('hr'));
          });
        })
        .catch(err => {
          console.error("Failed to load fixed assets:", err);
        });
    }
    
}
