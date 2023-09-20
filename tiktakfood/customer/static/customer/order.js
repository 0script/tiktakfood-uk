console.log(' customer order page ')
console.log('newer')

let button_add_orders=document.querySelectorAll('button.add-to-order');
console.log(button_add_orders)

let orders=document.querySelectorAll('.total-order');

orders.forEach(order=>{
  console.log(order)
})


document.querySelector('#whishlist-form').addEventListener('submit', (e) => {
    e.preventDefault();
});

function getCookie(cname) {
    let name = cname + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(';');
    for(let i = 0; i <ca.length; i++) {
      let c = ca[i];
      while (c.charAt(0) == ' ') {
        c = c.substring(1);
      }
      if (c.indexOf(name) == 0) {
        return c.substring(name.length, c.length);
      }
    }
    return ""
}


if(button_add_orders != []){
  console.log(button_add_orders)
  console.log('adding event ')
  
  button_add_orders.forEach(button=>{
    button.addEventListener('click',(e)=>{
      console.log(e.currentTarget.id);
      let item_quantity=e.currentTarget.id;
      console.log(document.cookie);
      console.log(getCookie('csrftoken'))
      console.log('requesdt')
      addToOrder(parseInt(item_quantity))
      console.log('sin gane')
  })
  })

//   button_add_orders.addEventListener('click',(e)=>{
//     console.log(e.currentTarget.id);
//     let item_quantity=e.currentTarget.id;
//     console.log(document.cookie);
//     console.log(getCookie('csrftoken'))
//     console.log('requesdt')
//     addToOrder(parseInt(item_quantity))
//     console.log('sin gane')
// })

}


async function addToOrder(item_quantity){

    let url='http://localhost:8000/customer/orders/';
    console.log('query')
    const response = await fetch(url, {
       method: "POST",
       headers: {
         "X-CSRFToken": getCookie("csrftoken"),
       },
       body: JSON.stringify({
            'item_quantity':item_quantity
        }),
     })
     .then(response => response.json())
     .then(data => {
    
       console.log(data.result)
       if(data.result=='success'){
        alert('Order created with success')
        window.location.reload();
       }else{
        alert('You must be loged in !');
       }
    });
}


let total_prices=document.querySelectorAll('.total-price')
let prices_list=document.querySelectorAll('.item-price')


total_prices.forEach(price=>{
  console.log('yoo'+price)
  let id=price.id;
  let total=0
  id=id.split('-')
  id=id[id.length-1]

  prices_list.forEach(price=>{
    let price_el=price.innerHTML
    price_el=price_el.split(' ')
    price_el=price_el[price_el.length-1]
    total+=parseInt(price_el)
    console.log(price_el)
  })
  price.innerHTML='Rwf '+total
  console.log(id)
})