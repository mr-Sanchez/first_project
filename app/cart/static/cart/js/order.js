
function calcTotal(discount) {
    var totalCost = localStorage.getItem('totalCost');
    var orderSum = document.querySelector('.orderSum');
    var orderDelivery = document.querySelector('.orderDelivery');
    var delivery = 150;
    orderDelivery.textContent = `${delivery} Руб.`;
    var orderTotal = document.querySelector('.orderTotal');
    orderDiscount = Math.round(parseInt(totalCost) / 100 * discount);
    console.log(orderDiscount);
    console.log(parseInt(totalCost) + delivery - orderDiscount);
    totalWithDiscount = (parseInt(totalCost) + delivery - orderDiscount).toString() + ' Руб.';
    orderSum.textContent = `${parseInt(totalCost) - orderDiscount} Руб.`;
    orderTotal.textContent = totalWithDiscount;
}

calcTotal(0);

var radios = document.querySelectorAll('input[type=radio][name="paymentMethod"]');
var deliveryAddress = document.querySelector('#inputAddress');
var inputCode = document.querySelector('#addCode');

function changeHandler(event) {
    let paymentMethod = document.querySelector('input[type=radio][name="paymentMethod"]:checked');
    if (paymentMethod && deliveryAddress.value) {
        console.log(paymentMethod.value + '---' + deliveryAddress.value);
        document.querySelector('#orderSubmit').disabled = false;
    }
}

if (radios) {
    Array.prototype.forEach.call(radios, function(radio) {
        radio.addEventListener('change', changeHandler);
    });
}

if (deliveryAddress) {
    deliveryAddress.addEventListener('keyup', changeHandler);
}

document.querySelector('#orderSubmit').onclick = function() {
    const xhr = new XMLHttpRequest();
    const requestURL = './create_purchase';
    xhr.open('POST', requestURL);
    var cart = localStorage.getItem('productsInCart');
    cart = JSON.parse(cart);
    console.log(coupons);
    var paymentMethod = document.querySelector('input[type=radio][name="paymentMethod"]:checked').value;
    var purchase = {'cart' : cart,
                    'discounts' : coupons,
                    'address' : deliveryAddress.value,
                    'paymentMethod' : paymentMethod
    };
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify(purchase));
    xhr.onload = function() {
        if (xhr.getResponseHeader('redirect') !== null) {
            window.location.replace(xhr.getResponseHeader('redirect'));
        }
        else {
            localStorage.removeItem('productsInCart')
            localStorage.setItem('totalCost', 0)
            localStorage.setItem('cartNumbers', 0)
            window.location.replace('./thanks')
        }
    }
}

var coupons = {};

inputCode.onclick = function() {
    var code = document.querySelector('#inputCode').value;
    fetch(`${window.origin}/cart/check_discount_code`, {
        method: "POST",
        credentials: "include",
        body: JSON.stringify(code),
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
            var inputCode = document.querySelector('#inputCode');
            inputCode.className = 'form-control';
            document.querySelector('.codeErrorCaption').innerHTML = '';
            var errorText = '';
            if (data['error']) {
                errorText = 'Скидочный код недействителен';
            }
            else {
                coupon_id = data['coupon_id'];
                if (!coupons) {
                    coupons = {
                        [coupon_id] : code
                    }
                }
                else if (coupons[coupon_id] === undefined) {
                    coupons = {
                        ...coupons,
                        [coupon_id] : code
                    }
                }
                else {
                    errorText = 'Скидочный код уже применен'
                }
            }

            if (errorText) {
                inputCode.classList.add('codeError');
                document.querySelector('.codeErrorCaption').innerHTML = `<span class="codeErrorCaption" style="color: red;">${errorText}</span>`;
            }
            else {
                calcTotal(data['coupon_discount']);
                let coupon = document.createElement('div');
                coupon.className = 'enteredCoupon';
                coupon.innerHTML = `${code} <span style="float: right;">скидка ${data['coupon_discount']}%</span>`;
                document.querySelector('.discountInputContainer').before(coupon);
                document.querySelector('#inputCode').value = '';
                document.querySelector('.orderSumContainer').insertAdjacentHTML('afterend', 
                '<div style="margin-bottom: 20px;"><span style="color:rgb(114, 114, 114)">Скидка на заказ</span><span class="orderDiscount" style="float: right;"></span></div>');
                document.querySelector('.orderDiscount').textContent = data['coupon_discount'].toString() + '%';
            }
        })
    })
};

