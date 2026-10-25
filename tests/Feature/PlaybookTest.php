<?php

namespace Tests\Feature;

use Illuminate\Support\Facades\Mail;
use Tests\TestCase;

class PlaybookTest extends TestCase
{
    public function test_signup_emails_the_owner_and_rejects_bad_input(): void
    {
        config(['mail.to' => 'owner@example.com']);
        $sent = fn () => Mail::mailer()->getSymfonyTransport()->messages();

        $this->postJson('/api/playbook', ['email' => 'not-an-email', 'guide' => 'Roofing', 'consent' => true])->assertStatus(422);
        $this->postJson('/api/playbook', ['email' => 'jo@example.com', 'guide' => 'Roofing', 'consent' => false])->assertStatus(422);
        $this->assertCount(0, $sent());

        $this->postJson('/api/playbook', ['email' => 'jo@example.com', 'guide' => 'Roofing', 'consent' => true])->assertNoContent();

        $email = $sent()->first()->getOriginalMessage();
        $this->assertSame('owner@example.com', $email->getTo()[0]->getAddress());
        $this->assertSame('jo@example.com', $email->getReplyTo()[0]->getAddress());
        $this->assertSame('Free playbook: Roofing', $email->getSubject());
    }
}
