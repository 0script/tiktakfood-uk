console.log('add order');
let add_to_whishlist_btn = document.querySelector("#add-whishlist-btn")
let add_order_btn=document.querySelector('#add-order-btn')

if(document.querySelector('#order-detail-form')){
    document.querySelector('#order-detail-form').addEventListener('submit', (e) => {
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
    return "";
}

if(add_to_whishlist_btn!=null){
    add_to_whishlist_btn.addEventListener('click',()=>{

        console.log('clicked');
        let quantity=document.querySelector('#quantity').value;
        let menu_id=document.querySelector('#menu-item-id').value;
    
        console.log(menu_id+'is '+quantity+typeof(menu_id));
    
        console.log(document.cookie);
        console.log(getCookie('csrftoken'))
    
        sendOrder(parseInt(menu_id),parseInt(quantity),false);
    
    });
}

if(add_order_btn!=null){
  add_order_btn.addEventListener('click',()=>{
    console.log('making order')
    let quantity=document.querySelector('#quantity').value;
    let menu_id=document.querySelector('#menu-item-id').value;
    
    sendOrder(parseInt(menu_id),parseInt(quantity),true)
  
  })
}


async function sendOrder(menu_id,quantity,order_now){

    let url='http://localhost:8000/restaurant/make-order/';
    console.log('query')
    const response = await fetch(url, {
       method: "POST",
       headers: {
         "X-CSRFToken": getCookie("csrftoken"),
       },
       body: JSON.stringify({
          'quantity':quantity,
          'menu_id':menu_id,
          'order_now':order_now
       }),
     })
     .then(response => response.json())
     .then(data => {
    
       console.log(data.result)
       if(data.result=='success'){
        alert('Order created with success')
        window.location.href='http://localhost:8000/customer/orders';
       }else{
        alert('You must be loged in !');
       }
    });
}