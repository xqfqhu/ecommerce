function edit_wishlist(
  e,
  productid,
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

      csrfmiddlewaretoken: csrfmiddlewaretoken,
      action: "post",
    },
    success: function (jsonReturned){
        success_action(jsonReturned,productid);
    },
    error: function (xhr, errmsg, err) {},
  });
}

function change_heart_color(jsonReturned, productid) {
  const black_heart_path =
    "M8 1.314C12.438-3.248 23.534 4.735 8 15-7.534 4.736 3.562-3.248 8 1.314z";
  const white_heart_path =
    "m8 2.748-.717-.737C5.6.281 2.514.878 1.4 3.053c-.523 1.023-.641 2.5.314 4.385.92 1.815 2.834 3.989 6.286 6.357 3.452-2.368 5.365-4.542 6.286-6.357.955-1.886.838-3.362.314-4.385C13.486.878 10.4.28 8.717 2.01L8 2.748zM8 15C-7.333 4.868 3.279-3.04 7.824 1.143c.06.055.119.112.176.171a3.12 3.12 0 0 1 .176-.17C12.72-3.042 23.333 4.867 8 15z";
  if (jsonReturned.wishlist_action == "add") {
    document
      .getElementById("heart_path" + productid)
      .setAttribute("d", black_heart_path);
  } else {
    document
      .getElementById("heart_path" + productid)
      .setAttribute("d", white_heart_path);
  }
}

function remove_card(jsonReturned, productid){
    document.getElementById("card" + productid).remove();
}
