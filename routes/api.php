<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\Facades\File;
use Illuminate\Support\Facades\Mail;
use Illuminate\Support\Facades\Route;
use Illuminate\Support\Str;
use Illuminate\Validation\Rule;

// The site's signup form posts here. The visitor gets their trade's playbook (public/playbooks/) by email, and you get a note.
// Each address gets one playbook a day at most, so nobody can use the form to flood someone's inbox.
Route::post('/playbook', function (Request $request) {
    $data = $request->validate([
        'email' => ['required', 'email', 'max:254'],
        'trade' => ['required', Rule::in(array_map(fn ($pdf) => basename($pdf, '.pdf'), File::glob(public_path('playbooks/*.pdf'))))],
        'consent' => ['accepted'],
    ]);
    $trade = Str::between(File::lines(base_path("playbooks/{$data['trade']}.md"))->first(), '# The ', ' Playbook');
    $send = Cache::add('playbook:'.sha1(strtolower($data['email'])), true, now()->addDay());

    if ($send) {
        $guide = url($data['trade']);
        $home = url('/');
        $text = <<<TEXT
            Hi,

            Thanks for asking! Your free {$trade} playbook is attached: what to say from the first call to the five-star review, with answers to the objections you'll hear most.

            The full start-up guide is here: {$guide}

            Questions? Just reply to this email.

            FollowThrough

            You're getting this because you asked for the playbook at {$home}. To get no more emails, reply with "unsubscribe".
            TEXT;
        Mail::raw($text, function ($message) use ($data, $trade) {
            $message->to($data['email'])
                ->replyTo(config('mail.to'))
                ->subject("Your free {$trade} playbook")
                ->attach(public_path("playbooks/{$data['trade']}.pdf"));
        });
    }

    $note = $send ? 'It was emailed to them automatically.' : 'They already got a playbook in the last day, so this one wasn\'t sent. Reply to send it by hand.';
    Mail::raw("{$data['email']} asked for the free {$trade} playbook. {$note}", function ($message) use ($data, $trade) {
        $message->to(config('mail.to'))
            ->replyTo($data['email'])
            ->subject('Free playbook: '.$trade);
    });

    return response()->noContent();
})->middleware('throttle:5,1');

// The Visibility Autopilot form posts here. Reply with the next steps (docs/01-business-plan.md, "How every plan starts").
Route::post('/plan', function (Request $request) {
    $data = $request->validate([
        'plan' => ['required', Rule::in(['Starter', 'Growth', 'Done-for-you', 'Not sure yet'])],
        'name' => ['required', 'string', 'max:120'],
        'business' => ['required', 'string', 'max:120'],
        'email' => ['required', 'email', 'max:254'],
        'phone' => ['nullable', 'string', 'max:40'],
        'message' => ['nullable', 'string', 'max:2000'],
        'consent' => ['accepted'],
    ]);

    $phone = $data['phone'] ?? 'not given';
    $message = $data['message'] ?? 'none';
    Mail::raw("Visibility Autopilot inquiry\n\nPlan: {$data['plan']}\nName: {$data['name']}\nBusiness: {$data['business']}\nEmail: {$data['email']}\nPhone: {$phone}\n\nMessage:\n{$message}\n\nReply to this email to answer them. How every plan starts: docs/01-business-plan.md", function ($mail) use ($data) {
        $mail->to(config('mail.to'))
            ->replyTo($data['email'])
            ->subject("Visibility Autopilot ({$data['plan']}): {$data['business']}");
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
