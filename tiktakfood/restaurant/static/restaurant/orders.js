console.log(' restaurant order page ')
console.log('newer')

let button_add_orders=document.querySelectorAll('button.add-to-order');
let total_prices=document.querySelectorAll('.total-price')
let prices_p_list=document.querySelectorAll('.item-price')

console.log('button add order '+button_add_orders)

if(document.querySelectorAll('.total-order')){
    let orders=document.querySelectorAll('.total-order');
    orders.forEach(order=>{
        console.log(order)
      })
}

if(document.querySelector('#restaurant-order-form')){
    document.querySelector('#restaurant-order-form').addEventListener('submit', (e) => {
        e.preventDefault();
    });
}


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

console.log('it is')
console.log(total_prices)

total_prices.forEach(price=>{

    console.log('yoo'+price)
    let id=price.id;
    let total=0
    id=id.split('-')
    id=id[id.length-1]
    console.log('the id is '+id)
    prices_p_list.forEach(price_p=>{
        let price_p_inner=price_p.innerHTML
        let price_p_id=price_p.id
        console.log('inner html '+price_p_inner)
        
        price_p_inner=price_p_inner.split(' ')
        price_p_inner=price_p_inner[price_p_inner.length-1]

        price_p_id=price_p_id.split('-')
        price_p_id=price_p_id[price_p_id.length-1]

        console.log('price_p_id '+price_p_id+'price_p_inner '+price_p_inner)

        if(price_p_id==id){
            total+=parseInt(price_p_inner)
        }
        
    })
  
    price.innerHTML='Rwf '+total

})