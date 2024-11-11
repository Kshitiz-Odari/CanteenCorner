var updateBtns = document.getElementsByClassName("update-cart");

for (var i = 0; i < updateBtns.length; i++) {
  updateBtns[i].addEventListener("click", function () {
    var productID = this.dataset.product;
    var action = this.dataset.action;
    if (user === "Guest") {
      addCookieItem(productID, action);
    } else {
      updateUserOrder(productID, action);
    }
  });
}

function addCookieItem(productID, action) {
  if (action == "add") {
    if (cart[productID] === undefined) {
      cart[productID] = { quantity: 1 };
    } else {
      cart[productID]["quantity"] += 1;
    }
  }

  if (action == "remove") {
    cart[productID]["quantity"] -= 1;
    if (cart[productID]["quantity"] <= 0) {
      console.log("Items should be deleted");
      delete cart[productID];
    }
  }
  document.cookie = "cart=" + JSON.stringify(cart) + ";domain=;path=/";
  location.reload();
}

function updateUserOrder(productID, action) {
  console.log("User logged in. Sending data.....");
  var url = "/update-item/";
  fetch(url, {
    method: "POST",
    headers: {
      "content-Type": "application/json",
      "X-CSRFTOKEN": csrftoken,
    },
    body: JSON.stringify({
      productID: productID,
      action: action,
    }),
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      console.log("data: ", data);
      location.reload();
    });
}
