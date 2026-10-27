<?php

namespace Tests\Feature;

use Illuminate\Support\Facades\Mail;
use Tests\TestCase;

class BadgeTest extends TestCase
{
    public function test_badge_order_emails_the_owner_and_rejects_bad_input(): void
    {
        config(['mail.to' => 'owner@example.com']);
        $sent = fn () => Mail::mailer()->getSymfonyTransport()->messages();
        $order = ['business' => 'Acme Roofing', 'website' => 'acmeroofing.com', 'email' => 'jo@example.com', 'consent' => true];

        $this->postJson('/api/badge', [...$order, 'email' => 'not-an-email'])->assertStatus(422);
        $this->postJson('/api/badge', [...$order, 'business' => ''])->assertStatus(422);
        $this->postJson('/api/badge', [...$order, 'consent' => false])->assertStatus(422);
        $this->assertCount(0, $sent());

        $this->postJson('/api/badge', $order)->assertNoContent();

        $email = $sent()->first()->getOriginalMessage();
        $this->assertSame('owner@example.com', $email->getTo()[0]->getAddress());
        $this->assertSame('jo@example.com', $email->getReplyTo()[0]->getAddress());
        $this->assertSame('Badge order: Acme Roofing', $email->getSubject());
        $this->assertStringContainsString('Google profile: not given', $email->getTextBody());
    }
}
