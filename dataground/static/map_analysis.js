$(document).ready(function() {
    $('#button1').click(function() {
        $('#content').html('<img src="/static/maps/Erangel.jpg" class="img-fluid" id="map-image">');
        setActiveButton(this);
        generateButtons(1);
    });
    $('#button2').click(function() {
        $('#content').html('<img src="/static/maps/Miramar.jpg" class="img-fluid" id="map-image">');
        setActiveButton(this);
        generateButtons(2);
    });
    $('#button3').click(function() {
        $('#content').html('<img src="/static/maps/Sanhok.jpg" class="img-fluid" id="map-image">');
        setActiveButton(this);
        generateButtons(3);
    });
    $('#button4').click(function() {
        $('#content').html('<img src="/static/maps/Vikendi.jpg" class="img-fluid" id="map-image">');
        setActiveButton(this);
        generateButtons(4);
    });
    $('#button5').click(function() {
        $('#content').html('<img src="/static/maps/Taego.jpg" class="img-fluid" id="map-image">');
        setActiveButton(this);
        generateButtons(5);
    });
    $('#button6').click(function() {
        $('#content').html('<img src="/static/maps/Deston.jpg" class="img-fluid" id="map-image">');
        setActiveButton(this);
        generateButtons(6);
    });
});

function setActiveButton(selectedButton) {
    $('.map-select-button').removeClass("active");
    $(selectedButton).addClass("active");
}

function generateButtons(buttonId) {
    var buttonsToShow = [];
    var sanhokButtons = 16;
    var elseButtons = 32;

    // 버튼을 생성하는 로직
    if (buttonId === 3) {
        for (var i = 1; i <= sanhokButtons; i++) {
            buttonsToShow.push('<button class="map-select-button" data-button-id="' + i + '">버튼 ' + i + '</button>');
        }
    }
    
    else {
        for (var i = 1; i <= elseButtons; i++) {
            buttonsToShow.push('<button class="map-select-button" data-button-id="' + i + '">버튼 ' + i + '</button>');
        }
    }

    setActiveButton($('.map-select-button[data-button-id="' + buttonId + '"]'));

    // 생성된 버튼들에 클릭 이벤트 추가
    $('.map-select-button').click(function() {
        var selectedButtonId = $(this).attr("data-button-id");
        setActiveButton(this);
        displayMapImage(selectedButtonId);
    });

    
    $('#content').append(buttonsToShow.join(''));
}
