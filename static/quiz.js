$(function () {
    const mains = [];
    const complements = [];

    function storeState() {
        mains.length = 0;
        complements.length = 0;

        $('#mains .quizbox').each(function () {
            mains.push($(this).data('color'));
        });

        $('#complements .quizbox').each(function () {
            complements.push($(this).data('color'));
        });

        console.log('Mains:', mains);
        console.log('Complements:', complements);

        const mainDisplays = $('.main-display');
        const complementDisplays = $('.complement-display');

        mainDisplays.each(function (i) {
            const el = $(this);
            const baseClasses = el.attr('class').split(' ').filter(c => c !== undefined && !mains.includes(c));
            el.attr('class', baseClasses.join(' '));
            if (i < mains.length) {
                el.addClass(mains[i]);
            }
        });

        complementDisplays.each(function (i) {
            const el = $(this);
            const baseClasses = el.attr('class').split(' ').filter(c => c !== undefined && !complements.includes(c));
            el.attr('class', baseClasses.join(' '));
            if (i < complements.length) {
                el.addClass(complements[i]);
            }
        });
    }
    $(".quizbox").draggable({
      revert: "invalid",
      helper: "original",
      cursor: "move"
    });

    $("#mains").droppable({
      drop: function (event, ui) {
        ui.draggable
          .detach()
          .css({ top: 0, left: 0 })
          .appendTo(this);
        storeState();
      }
    });

    $("#complements").droppable({
      drop: function (event, ui) {
        ui.draggable
          .detach()
          .css({ top: 0, left: 0 })
          .appendTo(this);
        storeState();
      }
    });

    $("#closet").droppable({
      drop: function (event, ui) {
        ui.draggable
          .detach()
          .css({ top: 0, left: 0 })
          .appendTo(this);
        storeState();
      }
    });
});
