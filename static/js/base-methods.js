  $(document).ready(function() {

    // The Main Example on the Top
    $('#main-example').popSelect({
      placeholderText: 'Select keywords',
      showTitle: false
      //autofocus: true
    });

    // Example 1: With Max Allowed
    $('#example1').popSelect({
      showTitle: false,
      maxAllowed: 2
    });

    // With Bottom Popover
    $('#example2').popSelect({
      showTitle: false,
      placeholderText: 'Click to Add More',
      position: 'bottom'
    });

    // With Pre Selected Values
    $('#example3').popSelect({
      showTitle: false,
      autoIncrease: true
    });

  });
  getMultipleSelectedValue = function()
  {
      var elements = [];
      var x = document.getElementsByClassName("popover-select-tags")[0];
      var y = x.getElementsByClassName("tag");
      for (var i = 0; i < y.length; i++) {
              elements.push($(y[i]).data('text'))
      }
      return elements;
};
addNewKeyword = function()
{
    var x = document.getElementsByClassName("popover-select-list")[0];
    var new_keyword = document.getElementById("new_keyword").value;
    $(x).append('<li data-value="'+new_keyword+'" data-text="'+new_keyword+'">'+new_keyword+'</li>')
};
function ClearFields() {

     document.getElementById("new_keyword").value = "";
};
function GetSelectedItem() {
  document.getElementById('keywords').value = getMultipleSelectedValue()
};

  !function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0],p=/^http:/.test(d.location)?'http':'https';if(!d.getElementById(id)){js=d.createElement(s);js.id=id;js.src=p+'://platform.twitter.com/widgets.js';fjs.parentNode.insertBefore(js,fjs);}}(document, 'script', 'twitter-wjs');
