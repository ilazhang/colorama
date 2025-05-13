$(function () {
    const mains = [];
    const complements = [];
    const mainBaseClass = 'border border-dark rounded-circle main-display';
    const complementBaseClass = 'border border-dark rounded-circle complement-display';

    function storeState() {
        mains.length = 0;
        complements.length = 0;

        $('#mains .quizbox').each(function () {
            mains.push($(this).data('id'));
        });

        $('#complements .quizbox').each(function () {
            complements.push($(this).data('id'));
        });

        console.log('Mains:', mains);
        console.log('Complements:', complements);

        const mainDisplays = $('.main-display');
        const complementDisplays = $('.complement-display');

        mainDisplays.each(function (i) {
            const el = $(this);
            if (i < mains.length) {
                const color = $('#mains .quizbox').eq(i).data('color');
                const newClass = mainBaseClass + ' ' + color;
                el.attr('class', newClass);
            } else {
                el.attr('class', mainBaseClass);
            }
        });

        complementDisplays.each(function (i) {
            const el = $(this);
            if (i < complements.length) {
                const color = $('#complements .quizbox').eq(i).data('color');
                const newClass = complementBaseClass + ' ' + color;
                el.attr('class', newClass);
            } else {
                el.attr('class', complementBaseClass);
            }
        });

        const totalSlots = mainDisplays.length + complementDisplays.length;
        const totalUsed = mains.length + complements.length;

        if (totalUsed >= totalSlots) {
            $('#see-answer').removeClass('d-none');
        } else {
            $('#see-answer').addClass('d-none');
        }
    }

    $('#see-answer').on('click', function () {
        const mainsParam = mains.join(',');
        const complementsParam = complements.join(',');
        window.location.href = `/quizanswer?mains=${encodeURIComponent(mainsParam)}&complements=${encodeURIComponent(complementsParam)}`;
    });

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
