console.log('orders btn js')

let orders_forms=document.querySelectorAll('.restaurant-orders-form')
let orders_button=document.querySelectorAll('button.orders-btn')

if(orders_forms != []){
    orders_forms.forEach( order =>{
        order.addEventListener('submit',(e)=>{
            e.preventDefault()
        })
    })
}



console.log('default prevent ok ')

if(orders_button != [] ){
    orders_button.forEach((btn)=>{
        
        btn.addEventListener('click',(e)=>{
            //console.log(e.currentTarget.classList)
            let order_id=e.currentTarget.classList
            let action=e.currentTarget.innerText
            let data={}
            if(action=='Ordered'){
                data={'ordered':true}
            }
            if(action=='Shipped'){
                data={'shipped':true}
            }
            if(action=='On the way'){
                data={'on-the-way':true}
            }
            if(action=='Delivered'){
                data={'delivered':true}
            }

            order_id=order_id[order_id.length-1]
            order_id=order_id.split('-')
            order_id=order_id[order_id.length-1]

            changeOrderStatus(data,order_id)
        })
        
    })
}

async function changeOrderStatus(action,order_id){

    let url='http://localhost:8000/restaurant/orders/';
    console.log('query')
    const response = await fetch(url, {
       method: "POST",
       headers: {
         "X-CSRFToken": getCookie("csrftoken"),
       },
       body: JSON.stringify({
            'action':action,
            'order':order_id
        }),
     })
     .then(response => response.json())
     .then(data => {
    
       console.log(data.result)
       if(data.result=='success'){
        alert('Order updated with success')
        window.location.reload();
       }else{
        alert('You must be loged in !');
       }
    });
}


console.log('pas bon pas bon')