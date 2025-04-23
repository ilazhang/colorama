$(function () {
    const mains = [];
    const complements = [];
    const mainBaseClass = 'border border-dark rounded-circle main-display';
    const complementBaseClass = 'border border-dark rounded-circle complement-display';

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
            const newClass = mainBaseClass + (i < mains.length ? ' ' + mains[i] : '');
            el.attr('class', newClass);
        });

        complementDisplays.each(function (i) {
            const el = $(this);
            const newClass = complementBaseClass + (i < complements.length ? ' ' + complements[i] : '');
            el.attr('class', newClass);
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
