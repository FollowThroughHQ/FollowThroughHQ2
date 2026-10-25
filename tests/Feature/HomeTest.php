<?php

namespace Tests\Feature;

use Tests\TestCase;

class HomeTest extends TestCase
{
    // The page is plain HTML in a Blade view; Blade must pass it through untouched.
    public function test_home_page_is_served_unchanged(): void
    {
        $this->get('/')->assertOk();
        $this->assertSame(file_get_contents(resource_path('views/home.blade.php')), $this->get('/')->getContent());
    }
}
