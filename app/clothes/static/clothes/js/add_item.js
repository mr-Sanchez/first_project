let cart = document.querySelector('.add-item');
let item_id = document.querySelector('#item_id');
let item_price = document.querySelector('#item_price');
let item_name = document.querySelector('#itemName');
let item_image = document.querySelector('.itemImage');

const cartNotification = {
    init() {
        this.hideTimeout = null;
        this.el = document.createElement('div');
        this.el.className = 'cartNotification';
        document.body.appendChild(this.el);
    },

    show(info, status) {
        clearTimeout(this.hideTimeout);
        if (status == 'accept') {
            this.el.innerHTML = "";
            this.el.innerHTML += `<img src="${info.itemImage}" style="width: 130px;">`
            this.el.innerHTML += `<div class="ntContent ntText"><span class="ntInfo">${info.itemName}</span><br><span class="ntInfo">${info.price} Руб</span><br><span class="ntSize">Размер: ${info.size}</span></div>`;
            this.el.innerHTML += `<a href="/cart"><div class="ntCart">КОРЗИНА: (${localStorage.getItem('cartNumbers')})</div></a>`;
        }
        else {
            this.el.innerHTML = `<div>${info}</div>`;
        }
        this.el.className = 'cartNotification cartNotification--visible';
        this.hideTimeout = setTimeout(() => {
            this.el.classList.remove('cartNotification--visible');
        }, 3000);
    }
}

document.addEventListener('DOMContentLoaded', () => cartNotification.init());

/*
size_list.addEventListener('change', function() {
    var selectedSize = this.value;
}); */

if (cart) {
    cart.addEventListener('click', () => {
        setItems();
    });
}


/*
function cartNumbers() {
         
} */

function setItems() {
    let cartItems = localStorage.getItem('productsInCart');
    cartItems = JSON.parse(cartItems);
    var size_id = document.querySelector('.form-select').value;
    fetch(`${window.origin}/clothes/check_size_count`, {
        method: "POST",
        credentials: "include",
        body: size_id,
        cache: "no-cache",
        headers: new Headers({
            "content-type" : "application/json"
        })
    })
    .then( function (response) {
        if (response.status !== 200) {
            console.log(`Response status was not 200: ${response.status}`);
            return ;
        }
        response.json().then(function (data) {
            let sizeCount = data['size_count'];
            let item_size = data['size_tag'];
            productInCartId = item_id.value + item_size;
            let img = item_image.src;
            /*
            let img = document.createElement('img'); 
            img.src = item_image.src;
            img.className = 'ntContent ntImage';*/

            let product = {
                id: item_id.value,
                itemName: item_name.textContent,
                itemImage: img,
                price: parseInt(item_price.textContent.split(" ")[0]),
                sizeId: size_id,
                size: item_size,
                inCart: 0
            }
            
            if (!cartItems) {
                cartItems = {
                    [productInCartId] : product
                }
            }
            if (cartItems[productInCartId] === undefined) {
                cartItems = {
                    ...cartItems,
                    [productInCartId] : product
                }
            }
            if (sizeCount > cartItems[productInCartId].inCart) {
                cartItems[productInCartId].inCart += 1;
                localStorage.setItem('productsInCart', JSON.stringify(cartItems));
                let productNumbers = localStorage.getItem('cartNumbers');
                productNumbers = parseInt(productNumbers);
                if (productNumbers) {
                    localStorage.setItem('cartNumbers', productNumbers + 1);
                } else {
                localStorage.setItem('cartNumbers', 1);
                }
                document.querySelector('.cart').textContent = localStorage.getItem('cartNumbers');
                totalCost(product.price);
                notificationInfo = product;
                status = 'accept';
            }
            else {
                notificationInfo = 'Невозможно добавить этот товар в данный момент';
                status = 'error';
            }
            cartNotification.show(notificationInfo, status);
        })
    })
}

function totalCost(price) {
    let cartCost = localStorage.getItem('totalCost');
    if (cartCost != null) {
        cartCost = parseInt(cartCost);
        localStorage.setItem('totalCost', cartCost + price);
    } else {
        localStorage.setItem('totalCost', price);
    }
}

function displayCart() {
    let cartItems = localStorage.getItem('productsInCart');
    cartItems = JSON.parse(cartItems);
    let productContainer = document.querySelector('.products');
    let cartCost = localStorage.getItem('totalCost');
    if (cartItems && productContainer) {
        productContainer.innerHTML = '';
        Object.entries(cartItems).map(([key, item]) => {
            productContainer.innerHTML += `
            <div class="product" id="prd-${key}">
                <div class="product-description">
                    <img src="/cart/static/cart/img/trash.svg" style="width: 25px; cursor: pointer;" onclick="removeAllItems('${key}');">
                    <img src="${item.itemImage}" style="width: 130px; padding-left: 30px; padding-right: 10px;">
                    <span>${item.itemName}</span>
                </div>
                    <div class="product-size">${item.size}</div>
                    <div class="product-price">${item.price} Руб.</div>
                    <div class="product-quantity">
                        <img src="/cart/static/cart/img/dash-circle.svg" style="width: 20px; cursor: pointer;" onclick="removeItem('${key}')">
                        <span id="product-incart" style="padding: 10px;">${item.inCart}</span>
                        <img src="/cart/static/cart/img/plus-circle.svg" style="width: 20px; cursor: pointer;" onclick="addItem('${key}')">
                    </div>
                    <div class="product-total">${item.inCart * item.price} Руб.</div>
            </div>
            `;
        });
        var productNumbers = localStorage.getItem('cartNumbers');
        productNumbers = parseInt(productNumbers);
        if (productNumbers != 0) {
            productContainer.innerHTML += `
            <div class="cartTotalContainer">
                <span class="cartTotalTitle">Общая стоимость товаров:</span>
                <span class="cartTotal">${cartCost} Руб.</span>
            </div>
            <form action="/cart/order" method="POST">
                <input name="cartData" type="hidden" value='${JSON.stringify(cartItems)}'>
                <button type="submit" class="btn btn-dark">Перейти к оформлению заказа</button>
            </form>
            `;
        }
        else {
            productContainer.innerHTML += `<div class="cartEmptyContainer">Ваша корзина пуста</div>`
        }
        
        var notifications = document.querySelector('.cart-ntf').value;
        if (notifications) {
            notifications = JSON.parse(notifications);
            for (let key in notifications) {
                item = document.querySelector(`#prd-${key}`);
                item.classList.add('item-ntf');
                notification = document.createElement('div');
                notification.className = 'cart-count-ntf';
                notification.innerHTML += notifications[key];
                item.after(notification);
            }
        }
    }
}


function removeAllItems(id) {
    let cartItems = localStorage.getItem('productsInCart');
    let productNumbers = localStorage.getItem('cartNumbers');
    productNumbers = parseInt(productNumbers);
    cartItems = JSON.parse(cartItems);
    quantity = cartItems[id]['inCart'];
    total_price = quantity * cartItems[id]['price'];
    delete cartItems[id];
    localStorage.setItem('productsInCart', JSON.stringify(cartItems));
    console.log(localStorage.getItem('productsInCart'));
    localStorage.setItem('cartNumbers', productNumbers - quantity);
    document.querySelector('.cart').textContent = localStorage.getItem('cartNumbers');
    totalCost(-total_price);
    displayCart();
}


function removeItem(id) {
    let cartItems = localStorage.getItem('productsInCart');
    let productNumbers = localStorage.getItem('cartNumbers');
    productNumbers = parseInt(productNumbers);
    cartItems = JSON.parse(cartItems);
    if (cartItems[id]['inCart'] != 1) {
        cartItems[id]['inCart']--;
        localStorage.setItem('cartNumbers', productNumbers - 1);
        document.querySelector('.cart').textContent = localStorage.getItem('cartNumbers');
        localStorage.setItem('productsInCart', JSON.stringify(cartItems));
        totalCost(-cartItems[id]['price']);
        displayCart();
    }
}


function addItem(id) {
    var cartItems = localStorage.getItem('productsInCart');
    cartItems = JSON.parse(cartItems);
    var productNumbers = localStorage.getItem('cartNumbers');
    productNumbers = parseInt(productNumbers);
    fetch(`${window.origin}/clothes/check_size_count`, {
        method: "POST",
        credentials: "include",
        body: cartItems[id]['sizeId'],
        cache: "no-cache",
        headers: new Headers({
            "content-type" : "application/json"
        })
    })
    .then( function (response) {
        if (response.status !== 200) {
            console.log(`Response status was not 200: ${response.status}`);
            return ;
        }
        response.json().then(function (data) {
            let sizeCount = data['size_count'];
            if (sizeCount > cartItems[id]['inCart']) {
                cartItems[id]['inCart']++;
                localStorage.setItem('cartNumbers', productNumbers + 1);
                document.querySelector('.cart').textContent = localStorage.getItem('cartNumbers');
                localStorage.setItem('productsInCart', JSON.stringify(cartItems));
                totalCost(cartItems[id]['price']);
                displayCart();
            }
            else {
                cartNotification.show('Выбрано максимальное количество для этого товара', 'error');
            }
        })
    })
}


var addCommentButton = document.querySelector('#addComment');

addCommentButton.addEventListener('click', () => {
    var InputAuthor = document.querySelector('#InputAuthor');
    var InputText = document.querySelector('#InputText');
    var ClothesId = window.location.href.split('/');
    ClothesId = ClothesId[ClothesId.length - 1];
    fetch(`${window.origin}/clothes/add_comment`, {
        method: "POST",
        credentials: "include",
        body: JSON.stringify({'id' : ClothesId, 'author' : InputAuthor.value, 'text' : InputText.value}),
        cache: "no-cache",
        headers: new Headers({
            "content-type" : "application/json"
        })
    })
    .then( function (response) {
        if (response.status !== 200) {
            console.log(`Response status was not 200: ${response.status}`);
            return ;
        }
        response.json().then(function (data) {
            InputAuthor.value = '';
            InputText.value = '';
            var comments = document.querySelector('.Comments');
            var comment = document.createElement('p');
            comment.style.marginBottom = '30px';
            comment.innerHTML = `<span style="text-decoration: underline;">${data['author']}</span><span style="float: right;">${data['date']}</span><br><br><span>${data['text']}</span><hr>`;
            comments.appendChild(comment);
            var succesNtf = document.createElement('div');
            succesNtf.innerHTML = '<div class="alert alert-dismissible alert-success fade show" role="alert">Ваш отзыв опубликован<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>'
            document.querySelector('#commentTitle').after(succesNtf);
        })
    })
});

