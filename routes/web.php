<?php

use Illuminate\Support\Facades\Route;

// The site is one page; its script shows the right part for each address (/roofing, /sales...).
// Trades come from the T list in the view, so a new trade gets its address without a change here.
preg_match_all('/^\{s:"([a-z-]+)"/m', file_get_contents(resource_path('views/home.blade.php')), $trades);
$pages = ['guides', 'sales', 'calculator', 'about', 'privacy', 'terms', 'disclaimer', 'affiliate', ...$trades[1]];

Route::view('/', 'home');
Route::view('/{page}', 'home')->whereIn('page', $pages);
Route::permanentRedirect('/moving-transportation', '/hauling-transportation');

// The list of pages for search engines.
Route::get('/sitemap.xml', fn () => response(
    '<?xml version="1.0" encoding="UTF-8"?>'."\n".'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    .collect(['', ...$pages])->map(fn ($page) => '<url><loc>'.url($page).'</loc></url>')->join('')
    .'</urlset>', 200, ['Content-Type' => 'application/xml']));
