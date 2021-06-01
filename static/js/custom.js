var designSize = document.querySelectorAll(".options .selects h4")
var tshirtSize = document.querySelectorAll(".upload .selects-2 h4")
var tshirtColor = document.querySelectorAll(".options .selects .color")
var tshirtData = document.querySelector(".tshirt-data")
var tshirtDesgin = document.querySelector(".tshirt img")
var tshirt = document.querySelector(".tshirt")
var quentity = document.querySelector(".quentity-input")
var quentityPlus = document.querySelector(".quentity-section #plus")
var quentityMinus = document.querySelector(".quentity-section #minus")


designSize[1].style.background = "black"
designSize[1].style.color = "white"
tshirtSize[3].style.background = "black"
tshirtSize[3].style.color = "white"
tshirtColor[0].style.border = "1px solid #111"

var quentityValue = Number.parseInt(quentity.value)

quentityPlus.addEventListener('click', () => {
	quentity.value = ++quentityValue
	tshirtData.dataset.quentity = quentity.value
})
quentityMinus.addEventListener('click', () => {
	if(quentityValue > 1){
		quentity.value = --quentityValue
		tshirtData.dataset.quentity = quentity.value
	}
})

designSize.forEach((item, i) => {
	item.addEventListener("click", () => {
		designSize.forEach((item, i) => {
			item.style.background = "#f4f4f4"
			item.style.color = "gray"
		})
		item.style.background = "black"
		item.style.color = "white"
		tshirtData.dataset.design_size = item.dataset.size
		tshirtDesgin.className = `design-` + item.dataset.size
	})
})

tshirtSize.forEach((item, i) => {
	item.addEventListener("click", () => {
		tshirtSize.forEach((item, i) => {
			item.style.background = "#f4f4f4"
			item.style.color = "gray"
		})
		item.style.background = "black"
		item.style.color = "white"
		tshirtData.dataset.tshirt_size = item.dataset.size
	})
})

tshirtColor.forEach((item, i) => {
	item.addEventListener("click", () => {
		tshirt.style.backgroundColor = item.dataset.color
		tshirtData.dataset.tshirt_color = item.dataset.color
	})
})

var designInput = document.querySelector(".design-input")
designInput.addEventListener("input", () => {
	const reader = new FileReader()
	reader.readAsDataURL(designInput.files[0])
	reader.onload = () => {
		tshirtDesgin.src = reader.result
	}
})

var orderForm = document.querySelector(".custom-order-form")
orderForm.addEventListener('submit', (e) => {
	e.preventDefault()
	var formData = new FormData(orderForm)
	formData.append('tshirt_size', tshirtData.dataset.tshirt_size)
	formData.append('design_size', tshirtData.dataset.design_size)
	formData.append('color', tshirtData.dataset.tshirt_color)
	formData.append('quentity', tshirtData.dataset.quentity)
	console.log(Array.from(formData))

	var url = '/custom/'
	fetch(url, {
		method: 'POST',
		body: formData
	})
	.then((res) => {
		window.location.assign('/cart/none')
	})
})
