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


// Rating
var rating_star = document.querySelector('.rating');
var rating = Number(rating_star.dataset.rating);
var int_rating = parseInt(rating);
var fraction = rating - int_rating;
for(let i=1; i<=int_rating; i++){
	rating_star.innerHTML += '<i class="fas fa-star"></i>';
}
if(fraction >= 0.5){
	rating_star.innerHTML += '<i class="fas fa-star-half-alt"></i>';
	int_rating++;
}
for(let i=int_rating+1; i<=5; i++){
	rating_star.innerHTML += '<i class="far fa-star"></i>';
}

// location navigation
var links = document.querySelectorAll('.category-options a');
links.forEach((link) => {
	link.href = link.href.replace('product/', '');
});

document.querySelector('.rating-submit').addEventListener('click', function(){
	var rating = document.querySelector('.rating-select').value;
	var user = this.dataset.user;
	var product = this.dataset.product;
	console.log('product: ', product, 'user: ', user, 'rating: ', rating);

	var url = '/rating_update/'
	fetch(url, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			'X-CSRFToken': csrftoken,
		},
		body: JSON.stringify({
			'productID': product,
			'user': user,
			'rating': rating
		})
	})
	.then((response) => {
		return response.json()
	})
	.then((data) => {
		console.log('data:', data)
		location.reload();
	})
});



//review
var review_btn = document.querySelectorAll('.review-submit');
review_btn.forEach((submit) => {
	submit.addEventListener('click', function(){
		var productID = this.dataset.product;
		var action = this.dataset.action;

		if(action == "add"){
			var review = document.querySelector('.review-text').value;
			console.log('productID: ', productID, ' action:', action, ' review:', review);

			var url = '/update_review/'
			fetch(url, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					'X-CSRFToken': csrftoken,
				},
				body: JSON.stringify({
					'productID': productID,
					'action': action,
					'review': review
				})
			})
			.then((response) => {
				return response.json();
			})
			.then((data) => {
				console.log(data);
				location.reload();
			})
		}
		else{
			var reviewID = this.dataset.review;
			var url = '/update_review/'
			fetch(url, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					'X-CSRFToken': csrftoken,
				},
				body: JSON.stringify({
					'productID': productID,
					'action': action,
					'reviewID': reviewID
				})
			})
			.then((response) => {
				return response.json();
			})
			.then((data) => {
				console.log(data);
				location.reload();
			})
		}
	});

});
