var updateBtns = document.getElementsByClassName('update-cart')

for( var i=0; i<updateBtns.length; i++ ){
    updateBtns[i].addEventListener('click',function(){
      var productId = this.dataset.product
      var action = this.dataset.action
      console.log('productId', productId,'action', action)
      console.log('USER',user)
      if(user == 'AnonymousUser'){

      }else{
        updateUserOreder(productId,action)
      }
    })
}

function updateUserOreder(productId,action){
  console.log('User is logged in, sending data..')

  var url = '/shop/update_item/'

  fetch(url,{
    method: 'POST',
    headers: {
      'Content-Type':'application/json',
      'X-CSRFToken':csrftoken,
    },
    body: JSON.stringify({'productId':productId,'action':action})
  })
  .then((response) =>{
    return response.json()
  })

  .then((data) =>{
    console.log('data:',data)
    location.reload()
  })

}



// if (localStorage.getItem('cart') == null) {
//     var cart = {};
//   }
//   else {
//     cart = JSON.parse(localStorage.getItem('cart'));
//     document.getElementById('cart').innerHTML = Object.keys(cart).length;
//   }
//   $('.cart').click(function () {
//     console.log('clicked');
//     var idstr = this.id.toString();
//     console.log(idstr);
//     if (cart[idstr] != undefined) {
//       cart[idstr] = cart[idstr] + 1;
//     }
//     else {
//       cart[idstr] = 1;
//     }
//     console.log(cart);
//     localStorage.setItem('cart', JSON.stringify(cart));
//     document.getElementById('cart').innerHTML = Object.keys(cart).length;
//   });