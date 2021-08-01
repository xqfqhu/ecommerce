function add_to_basket(
  e,
  productid,
  productqty,
  url,
  csrfmiddlewaretoken,
  success_action
) {
  e.preventDefault();

  $.ajax({
    type: "POST",
    url: url,
    data: {
      productid: productid,
      productqty: productqty,
      csrfmiddlewaretoken: csrfmiddlewaretoken,
      action: "post",
    },
    success: function (jsonReturned) {
      success_action(jsonReturned);
    },
    error: function (xhr, errmsg, err) {},
  });
}

function increment_basket_count(jsonReturned){
  document.getElementById("basket-qty").innerHTML = jsonReturned.qty;
}