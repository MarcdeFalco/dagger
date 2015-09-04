$(document).ready(function(){

function uniqId() {
  return Math.round(new Date().getTime() + (Math.random() * 100));
}

$('a[href^="/detail/"]').qtip({
    content: {
        text: function(event, api) {
            $.ajax({
                url: this.attr('href')
            })
            .then(function(content) {
                // Set the tooltip content upon successful retrieval
                // api.elements.title = $(content).find('#atom_title').text();
                var tooltip_id = 'mathtooltip' + uniqId(); //+ String($(this).uniqueId());
                api.elements.content.html(
                    '<div id="' + tooltip_id + '"><p>'
                    + $(content).find('#atom_text').html()
                    + '</p></div>');
                MathJax.Hub.Queue(["Typeset",MathJax.Hub,tooltip_id]);
                api.reposition();
            }, function(xhr, status, error) {
                // Upon failure... set the tooltip content to the status and error value
                api.set('content.text', status + ': ' + error);
            });

            return 'Chargement...'; // Set some initial text
        }
    },
    position:{
        corner:{
          target:'leftTop',
          tooltip:'bottomRight'
        }
    },
    events: {
        /*
        hide: function () {
            $(this).qtip('destroy');
        }
        */
    }
});

});

