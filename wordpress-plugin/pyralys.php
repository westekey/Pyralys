<?php
/**
 * Plugin Name: Pyralys - AI Content Generator
 * Plugin URI: https://pyralys.com
 * Description: Generate AI-powered social media content directly from WordPress using Pyralys AI.
 * Version: 1.0.0
 * Author: Pyralys
 * Author URI: https://pyralys.com
 * License: GPL v2 or later
 * License URI: https://www.gnu.org/licenses/gpl-2.0.html
 * Text Domain: pyralys
 * Requires at least: 5.8
 * Requires PHP: 7.4
 */

// Exit if accessed directly
if (!defined('ABSPATH')) {
    exit;
}

// Define plugin constants
define('PYRALYS_VERSION', '1.0.0');
define('PYRALYS_PLUGIN_DIR', plugin_dir_path(__FILE__));
define('PYRALYS_PLUGIN_URL', plugin_dir_url(__FILE__));
define('PYRALYS_API_URL', 'http://localhost:8000/api/v1');

/**
 * Main Pyralys Plugin Class
 */
class Pyralys_Plugin
{
    private static $instance = null;

    /**
     * Get plugin instance
     */
    public static function get_instance()
    {
        if (self::$instance === null) {
            self::$instance = new self();
        }
        return self::$instance;
    }

    /**
     * Constructor
     */
    private function __construct()
    {
        // Activation/Deactivation hooks
        register_activation_hook(__FILE__, array($this, 'activate'));
        register_deactivation_hook(__FILE__, array($this, 'deactivate'));

        // Initialize plugin
        add_action('init', array($this, 'init'));
        add_action('admin_menu', array($this, 'add_admin_menu'));
        add_action('admin_enqueue_scripts', array($this, 'enqueue_admin_scripts'));

        // Add meta box to post editor
        add_action('add_meta_boxes', array($this, 'add_meta_boxes'));
    }

    /**
     * Plugin activation
     */
    public function activate()
    {
        // Set default options
        if (!get_option('pyralys_api_url')) {
            update_option('pyralys_api_url', PYRALYS_API_URL);
        }
    }

    /**
     * Plugin deactivation
     */
    public function deactivate()
    {
        // Cleanup if needed
    }

    /**
     * Initialize plugin
     */
    public function init()
    {
        load_plugin_textdomain('pyralys', false, dirname(plugin_basename(__FILE__)) . '/languages');
    }

    /**
     * Add admin menu
     */
    public function add_admin_menu()
    {
        add_menu_page(
            __('Pyralys AI', 'pyralys'),
            __('Pyralys AI', 'pyralys'),
            'manage_options',
            'pyralys',
            array($this, 'render_admin_page'),
            'dashicons-superhero',
            30
        );

        add_submenu_page(
            'pyralys',
            __('Settings', 'pyralys'),
            __('Settings', 'pyralys'),
            'manage_options',
            'pyralys-settings',
            array($this, 'render_settings_page')
        );
    }

    /**
     * Enqueue admin scripts and styles
     */
    public function enqueue_admin_scripts($hook)
    {
        if (strpos($hook, 'pyralys') === false && $hook !== 'post.php' && $hook !== 'post-new.php') {
            return;
        }

        wp_enqueue_style(
            'pyralys-admin',
            PYRALYS_PLUGIN_URL . 'assets/css/admin.css',
            array(),
            PYRALYS_VERSION
        );

        wp_enqueue_script(
            'pyralys-admin',
            PYRALYS_PLUGIN_URL . 'assets/js/admin.js',
            array('jquery'),
            PYRALYS_VERSION,
            true
        );

        wp_localize_script('pyralys-admin', 'pyralysData', array(
            'ajaxUrl' => admin_url('admin-ajax.php'),
            'nonce' => wp_create_nonce('pyralys_nonce'),
            'apiUrl' => get_option('pyralys_api_url', PYRALYS_API_URL),
        ));
    }

    /**
     * Add meta boxes
     */
    public function add_meta_boxes()
    {
        add_meta_box(
            'pyralys_ai_generator',
            __('Pyralys AI Generator', 'pyralys'),
            array($this, 'render_meta_box'),
            'post',
            'side',
            'high'
        );
    }

    /**
     * Render meta box
     */
    public function render_meta_box($post)
    {
        ?>
        <div id="pyralys-meta-box">
            <p><?php _e('Generate AI content for this post using Pyralys.', 'pyralys'); ?></p>

            <div class="pyralys-field">
                <label><?php _e('Prompt:', 'pyralys'); ?></label>
                <textarea id="pyralys-prompt" rows="3" style="width: 100%;" placeholder="<?php _e('Describe the content you want to generate...', 'pyralys'); ?>"></textarea>
            </div>

            <div class="pyralys-field">
                <label><?php _e('Platform:', 'pyralys'); ?></label>
                <select id="pyralys-platform" style="width: 100%;">
                    <option value="wordpress"><?php _e('WordPress', 'pyralys'); ?></option>
                    <option value="instagram"><?php _e('Instagram', 'pyralys'); ?></option>
                    <option value="linkedin"><?php _e('LinkedIn', 'pyralys'); ?></option>
                    <option value="facebook"><?php _e('Facebook', 'pyralys'); ?></option>
                </select>
            </div>

            <div class="pyralys-field">
                <label><?php _e('Tone:', 'pyralys'); ?></label>
                <select id="pyralys-tone" style="width: 100%;">
                    <option value="casual"><?php _e('Casual', 'pyralys'); ?></option>
                    <option value="professional"><?php _e('Professional', 'pyralys'); ?></option>
                    <option value="funny"><?php _e('Funny', 'pyralys'); ?></option>
                    <option value="inspirational"><?php _e('Inspirational', 'pyralys'); ?></option>
                </select>
            </div>

            <button type="button" id="pyralys-generate-btn" class="button button-primary" style="width: 100%; margin-top: 10px;">
                <?php _e('Generate Content', 'pyralys'); ?>
            </button>

            <div id="pyralys-result" style="margin-top: 15px; display: none;">
                <h4><?php _e('Generated Content:', 'pyralys'); ?></h4>
                <div id="pyralys-content"></div>
                <button type="button" id="pyralys-insert-btn" class="button" style="width: 100%; margin-top: 10px;">
                    <?php _e('Insert into Post', 'pyralys'); ?>
                </button>
            </div>

            <div id="pyralys-error" style="margin-top: 10px; display: none; color: red;"></div>
            <div id="pyralys-loading" style="margin-top: 10px; display: none;">
                <span class="spinner is-active" style="float: none; margin: 0;"></span>
                <?php _e('Generating...', 'pyralys'); ?>
            </div>
        </div>
        <?php
    }

    /**
     * Render admin page
     */
    public function render_admin_page()
    {
        ?>
        <div class="wrap">
            <h1><?php _e('Pyralys AI Content Generator', 'pyralys'); ?></h1>

            <div class="pyralys-admin-container">
                <div class="pyralys-card">
                    <h2><?php _e('Welcome to Pyralys!', 'pyralys'); ?></h2>
                    <p><?php _e('Generate AI-powered content directly from your WordPress dashboard.', 'pyralys'); ?></p>

                    <h3><?php _e('Features:', 'pyralys'); ?></h3>
                    <ul>
                        <li><?php _e('✨ AI-powered caption generation', 'pyralys'); ?></li>
                        <li><?php _e('🖼️ DALL-E 3 image generation', 'pyralys'); ?></li>
                        <li><?php _e('🏷️ Smart hashtag suggestions', 'pyralys'); ?></li>
                        <li><?php _e('📝 Multi-platform optimization', 'pyralys'); ?></li>
                    </ul>

                    <h3><?php _e('How to Use:', 'pyralys'); ?></h3>
                    <ol>
                        <li><?php _e('Configure your Pyralys API connection in Settings', 'pyralys'); ?></li>
                        <li><?php _e('When creating a new post, look for the "Pyralys AI Generator" panel', 'pyralys'); ?></li>
                        <li><?php _e('Describe what you want to create', 'pyralys'); ?></li>
                        <li><?php _e('Click "Generate Content" and insert into your post!', 'pyralys'); ?></li>
                    </ol>

                    <p>
                        <a href="<?php echo admin_url('admin.php?page=pyralys-settings'); ?>" class="button button-primary">
                            <?php _e('Go to Settings', 'pyralys'); ?>
                        </a>
                        <a href="<?php echo admin_url('post-new.php'); ?>" class="button">
                            <?php _e('Create New Post', 'pyralys'); ?>
                        </a>
                    </p>
                </div>
            </div>
        </div>
        <?php
    }

    /**
     * Render settings page
     */
    public function render_settings_page()
    {
        if (isset($_POST['pyralys_settings_submit'])) {
            check_admin_referer('pyralys_settings');

            update_option('pyralys_api_url', sanitize_text_field($_POST['pyralys_api_url']));
            update_option('pyralys_api_token', sanitize_text_field($_POST['pyralys_api_token']));

            echo '<div class="notice notice-success"><p>' . __('Settings saved successfully!', 'pyralys') . '</p></div>';
        }

        $api_url = get_option('pyralys_api_url', PYRALYS_API_URL);
        $api_token = get_option('pyralys_api_token', '');
        ?>
        <div class="wrap">
            <h1><?php _e('Pyralys Settings', 'pyralys'); ?></h1>

            <form method="post" action="">
                <?php wp_nonce_field('pyralys_settings'); ?>

                <table class="form-table">
                    <tr>
                        <th scope="row">
                            <label for="pyralys_api_url"><?php _e('Pyralys API URL', 'pyralys'); ?></label>
                        </th>
                        <td>
                            <input type="url"
                                   id="pyralys_api_url"
                                   name="pyralys_api_url"
                                   value="<?php echo esc_attr($api_url); ?>"
                                   class="regular-text"
                                   required>
                            <p class="description">
                                <?php _e('The URL of your Pyralys API server (e.g., http://localhost:8000/api/v1)', 'pyralys'); ?>
                            </p>
                        </td>
                    </tr>
                    <tr>
                        <th scope="row">
                            <label for="pyralys_api_token"><?php _e('API Token', 'pyralys'); ?></label>
                        </th>
                        <td>
                            <input type="password"
                                   id="pyralys_api_token"
                                   name="pyralys_api_token"
                                   value="<?php echo esc_attr($api_token); ?>"
                                   class="regular-text">
                            <p class="description">
                                <?php _e('Your Pyralys API authentication token', 'pyralys'); ?>
                            </p>
                        </td>
                    </tr>
                </table>

                <?php submit_button(__('Save Settings', 'pyralys'), 'primary', 'pyralys_settings_submit'); ?>
            </form>

            <hr>

            <h2><?php _e('Connection Status', 'pyralys'); ?></h2>
            <button type="button" id="pyralys-test-connection" class="button">
                <?php _e('Test Connection', 'pyralys'); ?>
            </button>
            <div id="pyralys-connection-result" style="margin-top: 10px;"></div>
        </div>
        <?php
    }
}

// Initialize plugin
Pyralys_Plugin::get_instance();
