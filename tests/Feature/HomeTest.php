<?php

namespace Tests\Feature;

use Tests\TestCase;

class HomeTest extends TestCase
{
    // The pages are plain HTML in Blade views; Blade must pass them through untouched.
    public function test_pages_are_served_unchanged(): void
    {
        foreach (['/' => 'home', '/v2' => 'home-v2'] as $url => $view) {
            $this->get($url)->assertOk();
            $this->assertSame(file_get_contents(resource_path("views/$view.blade.php")), $this->get($url)->getContent());
        }
    }
}
