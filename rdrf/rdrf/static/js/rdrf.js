function hide_empty_menu() {
  var menu_element_count = $(".dropdown-menu-button ul li").length;

  if (menu_element_count == 0) {
    $(".dropdown-menu-button").hide();
  }
}

// Some pages can have larger banners than others, adjusting the top padding of the main content
// so that the banner doesn't overflow
function adjustContentTopPadding() {
  var navbarHeight = $(".navbar").height() || 0;
  var bannerHeight = $(".banner").height() || 0;
  var relativePadding = 36;

  if (navbarHeight === 0 && bannerHeight == 0) {
    // Both navbar and banner are missing, better not do anything
    return;
  }

  $("#content").css({
    "padding-top": navbarHeight + bannerHeight + relativePadding
  });
}
