/**
 * Pyralys WordPress Plugin - Admin JavaScript
 */
(function($) {
    'use strict';

    /**
     * Generate AI content
     */
    $('#pyralys-generate-btn').on('click', function() {
        const prompt = $('#pyralys-prompt').val().trim();
        const platform = $('#pyralys-platform').val();
        const tone = $('#pyralys-tone').val();

        if (!prompt) {
            alert('Please enter a prompt');
            return;
        }

        // Show loading, hide results/errors
        $('#pyralys-loading').show();
        $('#pyralys-result').hide();
        $('#pyralys-error').hide();

        // Call Pyralys API
        $.ajax({
            url: pyralysData.apiUrl + '/ai/generate-caption',
            type: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + pyralysData.apiToken
            },
            data: JSON.stringify({
                prompt: prompt,
                platform: platform,
                tone: tone
            }),
            success: function(response) {
                $('#pyralys-loading').hide();
                $('#pyralys-result').show();

                // Display generated content
                let content = '<div class="pyralys-generated-content">';
                content += '<h4>Caption:</h4>';
                content += '<p>' + response.caption.replace(/\n/g, '<br>') + '</p>';

                if (response.hashtags && response.hashtags.length > 0) {
                    content += '<h4>Hashtags:</h4>';
                    content += '<p>';
                    response.hashtags.forEach(function(tag) {
                        content += '<span class="pyralys-tag">#' + tag + '</span> ';
                    });
                    content += '</p>';
                }

                content += '</div>';

                $('#pyralys-content').html(content);

                // Store generated content for insertion
                $('#pyralys-result').data('caption', response.caption);
                $('#pyralys-result').data('hashtags', response.hashtags);
            },
            error: function(xhr) {
                $('#pyralys-loading').hide();
                $('#pyralys-error').show();

                let errorMsg = 'Failed to generate content';
                if (xhr.responseJSON && xhr.responseJSON.detail) {
                    errorMsg = xhr.responseJSON.detail;
                }

                $('#pyralys-error').text(errorMsg);
            }
        });
    });

    /**
     * Insert generated content into post
     */
    $('#pyralys-insert-btn').on('click', function() {
        const caption = $('#pyralys-result').data('caption');
        const hashtags = $('#pyralys-result').data('hashtags') || [];

        if (!caption) {
            return;
        }

        // Get WordPress editor
        if (typeof wp !== 'undefined' && wp.data && wp.data.select('core/editor')) {
            // Gutenberg editor
            const currentContent = wp.data.select('core/editor').getEditedPostContent();
            let newContent = caption.replace(/\n/g, '\n\n');

            if (hashtags.length > 0) {
                newContent += '\n\n' + hashtags.map(tag => '#' + tag).join(' ');
            }

            // Append to existing content
            wp.data.dispatch('core/editor').editPost({
                content: currentContent + '\n\n' + newContent
            });

            alert('Content inserted successfully!');
        } else if (typeof tinymce !== 'undefined') {
            // Classic editor
            const editor = tinymce.get('content');
            if (editor) {
                let content = caption.replace(/\n/g, '<br>');

                if (hashtags.length > 0) {
                    content += '<br><br>' + hashtags.map(tag => '#' + tag).join(' ');
                }

                editor.insertContent(content);
                alert('Content inserted successfully!');
            }
        } else {
            // Fallback: copy to clipboard
            const tempInput = $('<textarea>');
            $('body').append(tempInput);
            tempInput.val(caption + '\n\n' + hashtags.map(tag => '#' + tag).join(' ')).select();
            document.execCommand('copy');
            tempInput.remove();
            alert('Content copied to clipboard! Paste it into your post.');
        }
    });

    /**
     * Test API connection
     */
    $('#pyralys-test-connection').on('click', function() {
        const $button = $(this);
        const $result = $('#pyralys-connection-result');

        $button.prop('disabled', true);
        $result.html('<span class="spinner is-active" style="float: none;"></span> Testing connection...');

        $.ajax({
            url: pyralysData.apiUrl + '/auth/me',
            type: 'GET',
            headers: {
                'Authorization': 'Bearer ' + $('#pyralys_api_token').val()
            },
            success: function(response) {
                $result.html('<div class="notice notice-success inline"><p>✓ Connection successful! Logged in as: ' + response.email + '</p></div>');
                $button.prop('disabled', false);
            },
            error: function(xhr) {
                let errorMsg = 'Connection failed. Please check your API URL and token.';
                if (xhr.status === 401) {
                    errorMsg = 'Authentication failed. Please check your API token.';
                } else if (xhr.status === 0) {
                    errorMsg = 'Could not connect to API server. Please check the URL.';
                }

                $result.html('<div class="notice notice-error inline"><p>✗ ' + errorMsg + '</p></div>');
                $button.prop('disabled', false);
            }
        });
    });

    /**
     * Get API token from settings
     */
    function getApiToken() {
        const token = $('#pyralys_api_token').val();
        if (token) {
            pyralysData.apiToken = token;
        }
        return pyralysData.apiToken;
    }

    // Initialize API token
    getApiToken();

})(jQuery);
