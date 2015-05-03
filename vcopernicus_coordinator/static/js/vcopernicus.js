$(function() {
  // Create dashboard gauge
  var opts = {
    lines: 12,
    angle: 0.0,
    lineWidth: 0.01,
    pointer: {
      length: 1,
      strokeWidth: 0.035,
      color: '#000000'
    },
    limitMax: 'true', 
    colorStart: 'transparent',
    colorStop: 'transparent',
    strokeColor: 'transparent',
    generateGradient: true
  };
  var target = document.getElementById('dashboard');
  var gauge = new Gauge(target).setOptions(opts);
  gauge.maxValue = 100;
  gauge.animationSpeed = 32;
  gauge.set(0.01);

  // Button 1 events
  $('.button1 input').mousedown(function(e) {
    $.post('/devices/' + device + '/sensors/button1', 'true');
  });
  $('.button1 input').mouseup(function(e) {
    $.post('/devices/' + device + '/sensors/button1', 'false');
  });
  
  // Button 2 events
  $('.button2 input').mousedown(function(e) {
    $.post('/devices/' + device + '/sensors/button2', 'true');
  });
  $('.button2 input').mouseup(function(e) {
    $.post('/devices/' + device + '/sensors/button2', 'false');
  });
  
  // Motion sensor events
  $('.light div').mouseover(function(e) {
    $.post('/devices/' + device + '/sensors/motion', 'true');
    $.post('/devices/' + device + '/sensors/motion', 'false');
  });
  
  // Knob events
  knob_last = 0;
  $('.knob input').knob({'height': 40, 'change': function(v) {
    knob_now = Math.round(v)
    if (knob_last != knob_now) {
      knob_last = knob_now;
      $.post('/devices/' + device + '/sensors/knob', '' + knob_now);
    }
  }});

  // Updates source
  var source = new EventSource('/devices/' + device + '/stream');
  
  // LED1 update
  source.addEventListener('led1', function(e) {
    led1 = JSON.parse(e.data);
    if (led1) { $('.led1 div').css('background-color', '#F00').css('box-shadow', '0 0 16px #F00'); }
    else { $('.led1 div').css('background-color', 'transparent').css('box-shadow', '0 0 0 #000'); }
  }, false);
  
  // LED2 update
  source.addEventListener('led2', function(e) {
    led2 = JSON.parse(e.data);
    if (led2 != '000000') { $('.led2 div').css('background-color', '#' + led2).css('box-shadow', '0 0 16px #' + led2); }
    else { $('.led2 div').css('background-color', 'transparent').css('box-shadow', '0 0 0 #000'); }
  }, false);
  
  // Dashboard update
  source.addEventListener('dashboard', function(e) {
    dashboard = JSON.parse(e.data);
    gauge.set(dashboard / 100.0 * 89);
  }, false);
  
  // Remotely triggered scenario sheet update
  source.addEventListener('scenario', function(e) {
    $('.copernicus-scenario').css('background-image', 'url(\'' + e.data + '\')');
  }, false);
  
  // Manually triggered scenario sheet update
  $('.scenario > input').change(function(e) {
    $('.copernicus-scenario').css('background-image', 'url(\'' + URL.createObjectURL(e.target.files[0]) + '\')');
  });
  
  // Trigger device state restore
  $.get('/devices/' + device + '/sensors');
}); 
