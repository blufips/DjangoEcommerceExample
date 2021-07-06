var updateBtns = document.getElementsByClassName('update-cart');

for(var i = 0; i < updateBtns.length; i++){
  updateBtns[i].addEventListener('click', function(){
    var productId = this.dataset.product;
    var action = this.dataset.action;
    console.log('productId:', productId, 'action: ', action);
    console.log('USER: ', user);
    if (user == 'AnonymousUser') {
      addCookieItem(productId, action);
    }
    else {
      updateUserOrder(productId, action);
    }
  });
}


function addCookieItem(productId, action){
  console.log('Not logged in..')
  if ( action == 'add' ){
    if(cart[productId] == undefined ){
      cart[productId] = {'quantity':1};
    }
    else{
      cart[productId]['quantity'] += 1;
    }
  }
  else if ( action == 'remove' ) {
    if ( cart[productId]['quantity'] > 1){
      cart[productId]['quantity'] -= 1;
    }
    else {
      console.log('Remove Item');
      delete cart[productId]
    }
  }
  // ADD THE UPDATED CART IN THE COOKIES
  console.log('Cart: ', cart)
  document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
  // RELOAD THE PAGE
  location.reload()
}

function updateUserOrder(productId, action){
  console.log('User is logged in, sending data');
  var url = '/update_item/'
  fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken
    },
    body: JSON.stringify({
      'productId': productId,
      'action': action
    })
  })
  .then((response) => {
    return response.json();
  })
  .then((data) => {
    console.log('data: ', data);
    // RELOAD THE PAGE
    location.reload();
  })
}
