<?php

namespace Tests\Feature;

use Tests\TestCase;

class HomeTest extends TestCase
{
    // The page is plain HTML in a Blade view; Blade must pass it through untouched.
    public function test_page_is_served_unchanged(): void
    {
        $this->get('/')->assertOk();
        $this->assertSame(file_get_contents(resource_path('views/home.blade.php')), $this->get('/')->getContent());
    }

    // Every page the site links to, and every trade, opens at its own address and is in the sitemap.
    public function test_every_page_has_its_own_address(): void
    {
        $view = file_get_contents(resource_path('views/home.blade.php'));
        preg_match_all('/href=\\\\?["\']\/([a-z-]*)/', $view, $links);
        preg_match_all('/^\{s:"([a-z-]+)"/m', $view, $trades);
        $pages = array_unique([...$links[1], ...$trades[1]]);
        $this->assertContains('roofing', $pages);

        $sitemap = $this->get('/sitemap.xml')->assertOk()->getContent();
        foreach ($pages as $page) {
            $this->assertSame($view, $this->get('/'.$page)->assertOk()->getContent(), "/$page");
            $this->assertStringContainsString('<loc>'.url($page).'</loc>', $sitemap);
        }

        $this->get('/no-such-page')->assertNotFound();
        $this->get('/moving-transportation')->assertRedirect('/hauling-transportation');
    }
}
