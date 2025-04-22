// some JS goes here i guess


$(function () {
    $(".quizbox").draggable({
      revert: "invalid",
      helper: "original",
      cursor: "move"
    });

    $("#mains").droppable({
      drop: function (event, ui) {
        ui.draggable
          .detach()
          .css({ top: "", left: "", position: "" })  // removes absolute position
          .appendTo(this);
      }
    });

    $("#complements").droppable({
      drop: function (event, ui) {
        ui.draggable
          .detach()
          .css({ top: "", left: "", position: "" })  // removes absolute position
          .appendTo(this);
      }
    });
});
