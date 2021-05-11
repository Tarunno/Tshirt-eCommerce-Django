// CART //
var update_cart_btn = document.querySelectorAll('.update-cart');
update_cart_btn.forEach((btn) => {
	btn.addEventListener('click', function(){
		var productID = this.dataset.product;
		var action = this.dataset.action;
		console.log('productID: ', productID, 'action: ', action);
		addCookieItem(productID, action);
	});
});

function addCookieItem(productID, action){
	console.log("Cookie..");
	if(action == "add"){
		if(cart[productID] == undefined){
			cart[productID] = {'quentity':1};
		}
		else{
			cart[productID]['quentity'] += 1;
		}
	}
	else if(action == 'remove'){
		cart[productID]['quentity'] -= 1;
		if(cart[productID]['quentity'] <= 0){
			delete cart[productID];
		}
	}
	console.log('Cart Created!', cart)
	document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/";
	location.reload();
}

function update_user_order(productID, action){
	console.log("user is authenticated");

	var url = '/update_item/';
	fetch(url, {
		method: 'POST',
		headers:{
			'Content-Type': 'application/json',
			'X-CSRFToken': csrftoken,
		},
		body: JSON.stringify({
			'productID': productID,
			'action': action
		})
	})
	.then((response) => {
		return response.json();
	})
	.then((data) => {
		document.querySelector('.cart-number').innerHTML = data['quentity'];
	})
}



// CAROSOL //
var carosol_container = document.querySelector('.carosol-container'),
	carosol_container_inner = document.querySelector('.carosol-container-inner'),
	carosol_items = document.querySelectorAll('.carosol-container .item');

carosol_container_inner.style.width = carosol_items.length * 282 + 'px';

var left_btn = document.querySelector('.left'),
	right_btn = document.querySelector('.right');

left_btn.addEventListener('click', go_left);
right_btn.addEventListener('click', go_right);

var margin_now = 0;
var left_to_go = 0;
left_btn.style.display = 'none';

function go_right(){
	left_btn.style.display = 'inline';
	margin_now -= 280;
	left_to_go += 280;
	if(margin_now - 280 * 2 < -carosol_container_inner.offsetWidth){
		right_btn.style.display = 'none';
	}
	carosol_container_inner.style.marginLeft = margin_now + 'px';
}
function go_left(){
	right_btn.style.display = 'inline';
	left_to_go -= 280;
	margin_now += 280;
	if(left_to_go <= 0){
		left_btn.style.display = 'none';
		left_to_go = 0;
	}
	carosol_container_inner.style.marginLeft = margin_now + 'px';
}
