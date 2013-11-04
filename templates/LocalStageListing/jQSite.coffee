defaults = 
    builds:
        value: ''
        text: 'Select a Build'  
    versions:
        value: ''
        text: 'Select a Version'
            
jsonCall = (url, callback) ->
    $.getJSON url, callback

buildForm = (name, values=false, opt=false) ->
    vOpt = opt if opt
    vOpt = makeDef name if not opt 
    vOpt += makeOpt hV,hV for hV in values if values
    id = "#"+name
    $(id).html vOpt

makeOpt = (value, text) ->
    '<option value="'+value+'">'+text+'</option>'

makeDef = (name) ->
    makeOpt defaults[name].value, defaults[name].text

$("#builds").change () ->
    url = "staging/api/builds"
    url = "staging/api/build/" + $(this).val() if $(this).val()
    $.getJSON url, (data) ->
        buildForm "versions", data.buildSet

$(document).ready ()->
    $("#builds").html makeDef 'builds'
    $("#versions").html makeDef 'versions'
    $.getJSON "staging/api/builds/", (data) ->
        buildForm "builds", data.builds 
