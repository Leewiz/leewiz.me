function myFunction() {
  alert("hello leewiz");
}

function get_stops_by_borough(borough) {
  (function ($) {
    var selected_value = $("#id_borough").val();
    $.getJSON(
      "/gtfs-rt/subway/borough/stops",
      { borough: borough },
      function (res, textStatus) {
        var options = '<option value="" selected="seleted">----------</option>';
        $.each(res.data, function (i, item) {
          options +=
            '<option value="' + item.id + '">' + item.stop_name + "</option>";
        });
        $("#id_stop_name").html(options);
        $("select#id_stop_name option").each(function () {
          if ($(this).val() == selected_value)
            $(this).attr("selected", "selected");
        });
      }
    );
  })(django.jQuery);
}
