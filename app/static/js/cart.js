function addToCart(id, name, price) {
    fetch('/api/cart', {
        method: "post",
        body: JSON.stringify({
            "id": id,
            "name": name,
            "price": price
        }),
        headers: {
            'Content-Type': "application/json"
        }
    }).then(function (res) {
        return res.json();
    }).then(function (data) {
        console.info(data)
        let c = document.getElementsByClassName('cart-counter');
        for (d of c)
            d.innerText = data.total_quantity
    })
}

const productList = {
    '1':{
        'id':'1',
        'name':'Iphone 15 Pro Max',
        'price':20000000,
        'quantity':3
    },
    '2':{
        'id':'2',
        'name':'Ipad gen 9',
        'price':7000000,
        'quantity':7
    }
}


function buy(productList) {
    fetch('/api/order', {
        headers: {
            'Content-Type': "application/json"
        },
        body: JSON.stringify(productList),
        method: 'POST'
    }).then(res => res.json())
        .then(data => {
            console.log(data.message)
            location.href = `/order-result?order-id=${data['order-id']}`
        })
        .catch(err => console.log(err))
}
