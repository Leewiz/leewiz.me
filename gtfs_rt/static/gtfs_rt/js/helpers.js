function myFunction() {
  alert("hello leewiz");
}

function get_stops_by_borough(borough) {
  (function ($) {
    $.getJSON(
      "/gtfs-rt/subway/borough/stops",
      { borough: borough },
      function (res, textStatus) {
        var options = "";
        $.each(res.data, function (i, item) {
          options +=
            '<option value="' + item.id + '">' + item.stop_name + "</option>";
        });
        $("#id_stop_name").html(options);
        var selected_value = $("#id_stop_name").val();
        $("select#id_stop_name option").each(function () {
          if ($(this).val() == selected_value)
            $(this).attr("selected", "selected");
        });
      }
    );
  })(django.jQuery);
}

function get_time_to_next_train(stop_id) {
  (function ($) {
    $.getJSON(
      "/gtfs-rt/subway/borough/stops/times",
      { stop_id: stop_id },
      function (res, textStatus) {
        var html_times = "";
        var selected_value = $("#id_stop_name").val();
        $("select#id_stop_name option").each(function () {
          if ($(this).val() == selected_value) {
            $(this).attr("selected", "selected");
          } else if ($(this).val() != selected_value) {
            $(this).removeAttr("selected");
          }
        });
        $.each(res.data, function (i, item) {
          console.log(item);
        });
      }
    );
  })(django.jQuery);
}
