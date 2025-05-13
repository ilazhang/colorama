$(document).ready(function() {
    let currentLesson = 1;
    const totalLessons = 4;
    
    function updateLessonDisplay() {
      $('.lesson').removeClass('active');
      $('#lesson-' + currentLesson).addClass('active');
      $('.lesson-dot').removeClass('active');
      $('.lesson-dot[data-lesson="' + currentLesson + '"]').addClass('active');
      $('#previous-lesson').prop('disabled', currentLesson === 1);
      $('#blue-next-lesson').prop('disabled', currentLesson === totalLessons);
      
      const url = new URL(window.location);
      url.searchParams.set('lesson', currentLesson);
      window.history.pushState({}, '', url);
    }
    
    const urlParams = new URLSearchParams(window.location.search);
    const lessonParam = urlParams.get('lesson');
    if (lessonParam && !isNaN(lessonParam) && lessonParam > 0 && lessonParam <= totalLessons) {
      currentLesson = parseInt(lessonParam);
    }
    
    $('#blue-next-lesson').click(function() {
      if (currentLesson < totalLessons) {
        currentLesson++;
        updateLessonDisplay();
      }
    });
    
    $('#previous-lesson').click(function() {
      if (currentLesson > 1) {
        currentLesson--;
        updateLessonDisplay();
      }
    });
    
    $('.lesson-dot').click(function() {
      currentLesson = parseInt($(this).data('lesson'));
      updateLessonDisplay();
    });
    
    updateLessonDisplay();
    
    $('.color-circle-large, .color-circle-small').each(function() {
      const colorName = $(this).data('color-name');
      $(this).attr('title', colorName);
      
      //show color name on hover
      $(this).hover(
        function() {
          const label = $('<div class="color-label"></div>').text(colorName);
          $(this).append(label);
        },
        function() {
          $(this).find('.color-label').remove();
        }
      );
    });
    
    //click color circles to redirect to detail page
    $('.color-circle-large, .color-circle-small').click(function() {
      const colorName = $(this).data('color-name');
      const palette = $(this).data('palette');
      const color = $(this).data('color');
      
      window.location.href = '/color-detail?palette=' + encodeURIComponent(palette) + '&color=' + encodeURIComponent(color) + '&name=' + encodeURIComponent(colorName);
    });
  });