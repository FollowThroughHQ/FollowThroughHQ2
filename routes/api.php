<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Mail;
use Illuminate\Support\Facades\Route;

// The site's signup form posts here. The request lands in your inbox; hit Reply to send the playbook.
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
