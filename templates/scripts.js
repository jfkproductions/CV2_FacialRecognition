// scripts.js
// Update the label of the custom file input when a file is selected
$('#image').on('change', function(){
    var fileName = $(this).val().split('\\').pop();
    $(this).next('.custom-file-label').html('<i class="fas fa-upload"></i> ' + fileName);
    $('#loading-overlay').show();
    $('#upload-form').submit();
});

function updateMethodExplanation() {
    var method = $('#method').val();
    if (method === 'haarcascade') {
        $('#classifier-group').show();
        $('#parameters-group').show();
        $('#min-neighbors-group').show();
        $('#hog-parameters').hide();
        $('#upsample-times-group').hide();
        $('#method-explanation').html('<p><strong>Haar Cascade:</strong> Detects using a pre-trained model based on positive and negative images.</p>');
    } else if (method === 'HOG' || method === 'CNN') {
        $('#classifier-group').hide();
        $('#parameters-group').hide();
        $('#min-neighbors-group').hide();
        $('#hog-parameters').show();
        $('#upsample-times-group').show();
        if (method === 'HOG') {
            $('#method-explanation').html('<p><strong>HOG:</strong> Uses the distribution of intensity gradients to detect objects.</p>');
        } else {
            $('#method-explanation').html('<p><strong>CNN:</strong> A deep learning method using a convolutional neural network model.</p>');
        }
    }
}

$(document).ready(function() {
    updateMethodExplanation();
});

$('#method').on('change', function(){
    updateMethodExplanation();
});