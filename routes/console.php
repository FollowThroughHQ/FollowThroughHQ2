<?php

use Illuminate\Foundation\Inspiring;
use Illuminate\Support\Facades\Artisan;
use Illuminate\Support\Facades\File;
use Illuminate\Support\Facades\Process;
use Illuminate\Support\Str;
use League\CommonMark\Extension\SmartPunct\SmartPunctExtension;

Artisan::command('inspire', function () {
    $this->comment(Inspiring::quote());
})->purpose('Display an inspiring quote');

// Turns each playbooks/[slug].md into public/playbooks/[slug].pdf with Google Chrome. Files starting with _ are skipped.
Artisan::command('playbooks {slug?}', function (?string $slug = null) {
    $chrome = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
    $css = File::get(base_path('playbooks/style.css'));
    $fonts = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@700&display=block">';
    File::ensureDirectoryExists($tmp = storage_path('app/playbooks'));
    File::ensureDirectoryExists(public_path('playbooks'));

    foreach (File::glob(base_path('playbooks/'.($slug ?? '[a-z]*').'.md')) as $file) {
        $name = basename($file, '.md');
        $body = Str::markdown(File::get($file), ['renderer' => ['soft_break' => "<br>\n"]], [new SmartPunctExtension]);
        $title = Str::between($body, '<h1>', '</h1>');
        File::put($html = "$tmp/$name.html", "<!doctype html><html lang=\"en\"><meta charset=\"utf-8\"><title>$title</title>$fonts<style>$css</style>"
            ."<div class=\"logo\"><b>FT</b>FollowThrough</div>$body</html>");

        $result = Process::run([$chrome, '--headless', '--disable-gpu', '--no-pdf-header-footer', '--virtual-time-budget=5000',
            '--print-to-pdf='.public_path("playbooks/$name.pdf"), "file://$html"]);
        $result->successful() ? $this->info("public/playbooks/$name.pdf") : $this->error("$name: ".$result->errorOutput());
    }
})->purpose('Make the playbook PDFs from playbooks/*.md');
