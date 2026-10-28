<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Mail;
use Illuminate\Support\Facades\Route;

// The site's signup form posts here. The request lands in your inbox; hit Reply to send the playbook (public/playbooks/, docs/08).
Route::post('/playbook', function (Request $request) {
    $data = $request->validate([
        'email' => ['required', 'email', 'max:254'],
        'guide' => ['required', 'string', 'max:100'],
        'consent' => ['accepted'],
    ]);

    Mail::raw("Please send me the free {$data['guide']} playbook. My email: {$data['email']}", function ($message) use ($data) {
        $message->to(config('mail.to'))
            ->replyTo($data['email'])
            ->subject('Free playbook: '.$data['guide']);
    });

    return response()->noContent();
})->middleware('throttle:5,1');

// The badge order form posts here. Check the business, then reply with the result (docs/11-verified-badge.md).
Route::post('/badge', function (Request $request) {
    $data = $request->validate([
        'business' => ['required', 'string', 'max:120'],
        'website' => ['required', 'string', 'max:200'],
        'google' => ['nullable', 'string', 'max:500'],
        'email' => ['required', 'email', 'max:254'],
        'consent' => ['accepted'],
    ]);

    $google = $data['google'] ?? 'not given';
    Mail::raw("Verified Business badge order\n\nBusiness: {$data['business']}\nWebsite: {$data['website']}\nGoogle profile: {$google}\nEmail: {$data['email']}\n\nHow to check it and what to reply: docs/11-verified-badge.md", function ($message) use ($data) {
        $message->to(config('mail.to'))
            ->replyTo($data['email'])
            ->subject('Badge order: '.$data['business']);
    });

    return response()->noContent();
})->middleware('throttle:5,1');
