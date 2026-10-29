<?php

namespace Tests\Feature;

use Illuminate\Support\Facades\Mail;
use Tests\TestCase;

class PlanTest extends TestCase
{
    public function test_plan_inquiry_emails_the_owner_and_rejects_bad_input(): void
    {
        config(['mail.to' => 'owner@example.com']);
        $sent = fn () => Mail::mailer()->getSymfonyTransport()->messages();
        $inquiry = ['plan' => 'Growth', 'name' => 'Jo Smith', 'business' => 'Acme Roofing', 'email' => 'jo@example.com', 'consent' => true];

        $this->postJson('/api/plan', [...$inquiry, 'email' => 'not-an-email'])->assertStatus(422);
        $this->postJson('/api/plan', [...$inquiry, 'plan' => 'Gold'])->assertStatus(422);
        $this->postJson('/api/plan', [...$inquiry, 'name' => ''])->assertStatus(422);
        $this->postJson('/api/plan', [...$inquiry, 'consent' => false])->assertStatus(422);
        $this->assertCount(0, $sent());

        $this->postJson('/api/plan', [...$inquiry, 'message' => 'Do you cover Ohio?'])->assertNoContent();

        $email = $sent()->first()->getOriginalMessage();
        $this->assertSame('owner@example.com', $email->getTo()[0]->getAddress());
        $this->assertSame('jo@example.com', $email->getReplyTo()[0]->getAddress());
        $this->assertSame('Visibility Autopilot (Growth): Acme Roofing', $email->getSubject());
        $this->assertStringContainsString('Phone: not given', $email->getTextBody());
        $this->assertStringContainsString('Do you cover Ohio?', $email->getTextBody());
    }
}
