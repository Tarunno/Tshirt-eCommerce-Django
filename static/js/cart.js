var update_btn = document.querySelectorAll('.update-item');
var totalItem = document.querySelector('.total-item');

if(totalItem.innerHTML == 0){
	document.cookie ='cart=' + JSON.stringify({}) + ";domain=;path=/";
}

update_btn.forEach((btn) => {
	btn.addEventListener('click', function(){
		var productID = this.dataset.product;
		var action = this.dataset.action;

		console.log('productID: ', productID, 'action: ', action);
		console.log(user);
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

function update_user_item(productID, action){
	console.log("User is authenticated");

	var url = '/update_item/';

	fetch(url, {
		method: 'POST',
		headers: {
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
		console.log('data: ', data);
		location.reload();
	})
}
