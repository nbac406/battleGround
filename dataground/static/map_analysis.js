$(document).ready(function() {
    showInitialMessage();
    $('#button1').click(function() {
        $('#content').html('<img src="/static/maps/Erangel.jpg" class="img-fluid" id="map-image">');
        setActiveButton(this);
        generateInputFields();
        mapRequest('Erangel');
    });
    $('#button2').click(function() {
        $('#content').html('<img src="/static/maps/Miramar.jpg" class="img-fluid" id="map-image">');
        setActiveButton(this);
        generateInputFields();
        mapRequest('Miramar');
    });
    $('#button3').click(function() {
        $('#content').html('<img src="/static/maps/Sanhok.jpg" class="img-fluid" id="map-image">');
        setActiveButton(this);
        generateInputFields();
        mapRequest('Sanhok');
    });
    $('#button4').click(function() {
        $('#content').html('<img src="/static/maps/Vikendi.jpg" class="img-fluid" id="map-image">');
        setActiveButton(this);
        generateInputFields();
        mapRequest('Vikendi');
    });
    $('#button5').click(function() {
        $('#content').html('<img src="/static/maps/Taego.jpg" class="img-fluid" id="map-image">');
        setActiveButton(this);
        generateInputFields();
        mapRequest('Taego');
    });
    $('#button6').click(function() {
        $('#content').html('<img src="/static/maps/Deston.jpg" class="img-fluid" id="map-image">');
        setActiveButton(this);
        generateInputFields();
        mapRequest('Deston');
    });
});

function setActiveButton(selectedButton) {
    $('.map-select-button').removeClass("active");
    $(selectedButton).addClass("active");
}

function generateInputFields() {
    // airplaine-direction 내부의 입력 필드를 초기화
    $('.info').empty();
    $('.airplaine-direction').empty();

    // 두 개의 입력 필드 생성 및 추가
    let textField = '<h4>비행기의 출발지와 도착지를 입력해 주세요!</h4><br>'
    let inputField1 = '<input type="text" id="input-start" class="input-field" placeholder="출발">';
    let inputField2 = '<input type="text" id="input-destination" class="input-field" placeholder="도착">';
    let submitButton = '<button id="submit-button">확인</button>';
    let resetButton = '<button id="reset-button">리셋</button>';
    $('.info').append(textField);
    $('.airplaine-direction').append(inputField1, inputField2, submitButton, resetButton);
}

function mapRequest(mapName) {
    const submitButton = $('#submit-button');
    const resetButton = $('#reset-button'); // 리셋 버튼 추가

    submitButton.click(function() {
        event.preventDefault();
        // 입력된 출발지와 도착지 값을 가져옵니다.
        const start = $('#input-start').val();
        const destination = $('#input-destination').val();
        const csrfToken = getCookie('csrftoken');
        console.log(start, destination, mapName)

        // 서버와 통신하여 이미지 URL 가져오기
        $.ajax({
            url: '/getMapImageURL',
            type: 'POST',
            data: { start, destination, mapName },
            headers: {
                'X-CSRFToken': csrfToken
            },
            success: function(data) {
                const content = $('#content')
                // 성공 시 이미지 출력
                content.html(`<img src="${data.imageURL}" class="img-fluid" id="map-image">`);
            },
            error: function(xhr, textStatus, errorThrown) {
                // 실패 시 에러 처리
                console.error('Error:', errorThrown);
                $('#content').html('<h4>유효하지 않거나 표본이 적은 비행기 경로 입니다!!</h4>');
            }
        });
    });

    resetButton.click(function(event) {
        event.preventDefault();
        $('.info').empty();
        $('.airplaine-direction').empty();
        $('#content').html(`<img src="/static/maps/${mapName}.jpg" class="img-fluid" id="map-image">`);
        setActiveButton(this);
        generateInputFields();
        mapRequest(mapName);
    });
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function showInitialMessage(mapName) {
    $('#content').append('<h2>맵을 선택하시고 비행기 경로를 지정해 주시면</h2>');
    $('#content').append('<h2>해당 경로에서 유저들의 착륙지점들을 보여드립니다!</h2>');
}