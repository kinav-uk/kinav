// Kinav content: guides, kits, benefits rules and helplines.
// Facts checked against GOV.UK, Age UK and Alzheimer's Society (October 2026).
window.KC = {
  helplines: [
    { name: "Admiral Nurse Dementia Helpline", number: "0800 888 6678", note: "Dementia UK. Specialist dementia nurses." },
    { name: "Alzheimer's Society Dementia Support Line", number: "0333 150 3456", note: "Advice and someone to talk to." },
    { name: "Parkinson's UK Helpline", number: "0808 800 0303", note: "Free advice from Parkinson's nurses and advisers." },
    { name: "Stroke Association Helpline", number: "0303 3033 100", note: "For stroke survivors and their families." },
    { name: "British Heart Foundation Heart Helpline", number: "0808 802 1234", note: "Cardiac nurses for patients and families." },
    { name: "Samaritans", number: "116 123", note: "Any time, day or night. Free." }
  ],

  plans: {
    dementia: { kind: "condition", name: "Dementia", title: "Just diagnosed: dementia", lede: "Your first 30 days after a dementia diagnosis, one step at a time.", groups: [

    { title: "Week 1: get support in place", items: [
      { id: "a1", text: "Get the diagnosis in writing and a named contact", note: "From the GP or memory clinic." },
      { id: "a2", text: "Save the helpline numbers", note: "Admiral Nurses 0800 888 6678 · Alzheimer's Society 0333 150 3456" },
      { id: "a3", text: "Tell the DVLA and the car insurer", note: "Telling the DVLA is a legal requirement. Not telling them risks a fine of up to £1,000." },
      { id: "a4", text: "Ask the council for a free OT home assessment", note: "An occupational therapist checks the home before any fall or crisis. See the Home safety kit." }
    ]},
    { title: "Weeks 2 to 3: legal and money", items: [
      { id: "b1", text: "Make both Lasting Powers of Attorney", note: "Property and financial affairs, and health and welfare. Do it while they can still decide." },
      { id: "b2", text: "Check their will is up to date", note: "" },
      { id: "b3", text: "Claim Attendance Allowance", note: "Not means-tested. Use the Benefits calculator to see what else may apply." },
      { id: "b4", text: "Ask the council about a council tax discount", note: "Up to 100% off for severe mental impairment, with a GP certificate." }
    ]},
    { title: "Weeks 3 to 4: care and you", items: [
      { id: "c1", text: "Ask the council for a needs assessment and a carer's assessment", note: "Both are free, whatever their savings." },
      { id: "c2", text: "Check Carer's Allowance and Carer's Credit", note: "Carer's Credit from 20 hours a week, Carer's Allowance from 35." },
      { id: "c3", text: "Book a free fire safety visit", note: "From your local fire and rescue service." },
      { id: "c4", text: "Tell your employer", note: "One week of unpaid carer's leave a year, and the right to ask for flexible working, both from day one." },
      { id: "c5", text: "Ask the GP to record consent for you to discuss their care", note: "A signed letter from your parent is enough in the early stages." }
    ]}
    ]},
    parkinsons: { kind: "condition", name: "Parkinson's", title: "Just diagnosed: Parkinson's", lede: "Your first 30 days after a Parkinson's diagnosis, one step at a time.", groups: [
    { title: "Week 1: get support in place", items: [
      { id: "p-a1", text: "Ask for a Parkinson's nurse", note: "Ask the neurologist or GP for a referral to a Parkinson's nurse specialist, your main contact between appointments." },
      { id: "p-a2", text: "Save the Parkinson's UK helpline", note: "0808 800 0303. Free advice from nurses and advisers." },
      { id: "p-a3", text: "Tell the DVLA and the car insurer", note: "Parkinson's must be reported to the DVLA. Not telling them risks a fine of up to £1,000." },
      { id: "p-a4", text: "Ask the Parkinson's nurse about medicine timings", note: "Ask what timings matter, and set phone reminders if that helps." }
    ]},
    { title: "Weeks 2 to 3: therapy and money", items: [
      { id: "p-b1", text: "Ask for therapy referrals", note: "Physiotherapy for movement and balance, occupational therapy for daily tasks, and speech and language therapy for speech or swallowing." },
      { id: "p-b2", text: "Ask the physio about exercise", note: "Ask what's right for them, and about local Parkinson's groups." },
      { id: "p-b3", text: "Claim Attendance Allowance or PIP", note: "Attendance Allowance if over State Pension age, Personal Independence Payment if under. Use the Benefits calculator." },
      { id: "p-b4", text: "Make both Lasting Powers of Attorney", note: "Property and financial affairs, and health and welfare, while they can make the decision." }
    ]},
    { title: "Weeks 3 to 4: home, care and you", items: [
      { id: "p-c1", text: "Ask the council for a free OT home assessment", note: "To reduce falls and make daily tasks easier. See the Home safety kit." },
      { id: "p-c2", text: "Ask the council for a needs assessment and a carer's assessment", note: "Both are free, whatever their savings." },
      { id: "p-c3", text: "Check Carer's Allowance and Carer's Credit", note: "Carer's Credit from 20 hours a week, Carer's Allowance from 35." },
      { id: "p-c4", text: "Tell your employer", note: "One week of unpaid carer's leave a year, and the right to ask for flexible working, both from day one." },
      { id: "p-c5", text: "Ask the GP to record consent for you to discuss their care", note: "A signed letter from your parent is enough while they can decide." }
    ]}
    ]},
    mobility: { kind: "condition", name: "Poor mobility", title: "Poor mobility and falls", lede: "Your first 30 days of help when moving around gets harder, one step at a time.", groups: [
    { title: "Week 1: safety first", items: [
      { id: "m-a1", text: "Ask the GP for a falls check and a medicines review", note: "Some medicines raise the risk of falls. Ask about the local falls prevention service." },
      { id: "m-a2", text: "Ask the council for a free OT home assessment", note: "Equipment and small changes under £1,000 should be free in England." },
      { id: "m-a3", text: "Set up a fall alarm", note: "See the Fall alarms and home cameras kit." },
      { id: "m-a4", text: "Make the home safer today", note: "Remove loose rugs and clutter, add night lights, and keep a phone within reach." }
    ]},
    { title: "Weeks 2 to 3: strength and money", items: [
      { id: "m-b1", text: "Ask for a physiotherapy referral", note: "Strength and balance exercises reduce falls. Ask about walking aids too." },
      { id: "m-b2", text: "Book an eye test and a hearing check", note: "NHS eye tests are free for over-60s. Poor sight and hearing raise the risk of falls." },
      { id: "m-b3", text: "Claim Attendance Allowance or PIP", note: "Use the Benefits calculator." },
      { id: "m-b4", text: "Apply for a Blue Badge", note: "Parking close to where they need to go." }
    ]},
    { title: "Weeks 3 to 4: bigger changes and you", items: [
      { id: "m-c1", text: "Ask about a Disabled Facilities Grant", note: "Up to £30,000 in England for a stairlift, level-access shower or ramp. Means-tested." },
      { id: "m-c2", text: "Check feet and footwear", note: "Well-fitting shoes with a good grip help. Ask the GP about NHS podiatry." },
      { id: "m-c3", text: "Ask the council for a needs assessment and a carer's assessment", note: "Both are free, whatever their savings." },
      { id: "m-c4", text: "Make both Lasting Powers of Attorney", note: "Plan ahead while they can make the decision." },
      { id: "m-c5", text: "Tell your employer", note: "One week of unpaid carer's leave a year, and the right to ask for flexible working, both from day one." }
    ]}
    ]},
    stroke: {"name": "Stroke", "title": "After a stroke", "lede": "Your first 30 days after a stroke, one step at a time.", "kind": "condition", "groups": [{"title": "Week 1: in hospital and coming home", "items": [{"id": "stroke-0-0", "text": "Ask the stroke team what to watch for", "note": "Ask what signs mean you should call 999, and write it down. The NHS website explains stroke symptoms."}, {"id": "stroke-0-1", "text": "Save the Stroke Association helpline", "note": "0303 3033 100. Advice for stroke survivors and families."}, {"id": "stroke-0-2", "text": "Ask who is planning discharge, and for the plan in writing", "note": "See the Leaving hospital kit."}, {"id": "stroke-0-3", "text": "Ask about early supported discharge and rehab", "note": "Many areas offer therapy at home straight after hospital: physio, OT and speech and language therapy."}, {"id": "stroke-0-4", "text": "Stop driving and check the DVLA rules", "note": "They must not drive for a calendar month after a stroke, and must tell the DVLA if problems remain after that."}]}, {"title": "Weeks 2 to 3: recovery and money", "items": [{"id": "stroke-1-0", "text": "Keep a list of their medicines", "note": "Take it to every appointment. Ask the pharmacist or GP any questions about it."}, {"id": "stroke-1-1", "text": "Ask about a 6-month review", "note": "Everyone should have a review about 6 months after a stroke. Ask the GP or stroke team."}, {"id": "stroke-1-2", "text": "Claim Attendance Allowance or PIP", "note": "Attendance Allowance if over State Pension age, Personal Independence Payment if under. Use the Benefits calculator."}, {"id": "stroke-1-3", "text": "Ask the council for a free OT home assessment", "note": "Equipment and small changes under £1,000 should be free in England."}]}, {"title": "Weeks 3 to 4: care and you", "items": [{"id": "stroke-2-0", "text": "Ask the council for a needs assessment and a carer's assessment", "note": "Both are free, whatever their savings."}, {"id": "stroke-2-1", "text": "Make both Lasting Powers of Attorney", "note": "Property and financial affairs, and health and welfare, while they can make the decision."}, {"id": "stroke-2-2", "text": "Check Carer's Allowance and Carer's Credit", "note": "Carer's Credit from 20 hours a week, Carer's Allowance from 35."}, {"id": "stroke-2-3", "text": "Tell your employer", "note": "One week of unpaid carer's leave a year, and the right to ask for flexible working, both from day one."}]}]},
    eol: {"name": "End of life care", "title": "End of life care", "lede": "Making the last months as comfortable as possible, and knowing what to do.", "kind": "condition", "groups": [{"title": "Week 1: support and comfort", "items": [{"id": "eol-0-0", "text": "Ask the GP about palliative care", "note": "Ask for a referral to the local palliative care team or hospice. Hospices also support people at home."}, {"id": "eol-0-1", "text": "Save the Marie Curie Support Line", "note": "0800 090 2309. Practical and emotional support, for them and for you."}, {"id": "eol-0-2", "text": "Ask about NHS Continuing Healthcare fast track", "note": "If health is declining quickly, the NHS can fund care urgently. The GP or nurse completes the form."}, {"id": "eol-0-3", "text": "Ask about benefits under the special rules", "note": "If they may have 12 months or less to live, benefits such as Attendance Allowance can be paid faster at the highest rate. A doctor or nurse completes form SR1."}]}, {"title": "Weeks 2 to 3: their wishes", "items": [{"id": "eol-1-0", "text": "Talk about what matters to them", "note": "Where they want to be cared for, who they want with them, and any religious or cultural wishes."}, {"id": "eol-1-1", "text": "Ask about an advance care plan", "note": "Ask the GP about a ReSPECT form or advance care plan, and whether they want a DNACPR decision recorded."}, {"id": "eol-1-2", "text": "Check their will and Lasting Powers of Attorney", "note": "A will, and both Lasting Powers of Attorney, if not already made."}, {"id": "eol-1-3", "text": "Ask about equipment and night support", "note": "Hospital bed, commode, and night sitters from the hospice or Marie Curie."}]}, {"title": "Weeks 3 to 4: preparing", "items": [{"id": "eol-2-0", "text": "Know who to call, day and night", "note": "Keep the numbers for the GP, district nurse, out-of-hours service and hospice in one place."}, {"id": "eol-2-1", "text": "Ask about anticipatory medicines", "note": "Medicines kept at home in case symptoms such as pain or breathlessness appear suddenly."}, {"id": "eol-2-2", "text": "Know what happens after a death", "note": "A doctor confirms the death and issues the medical certificate. Register the death within 5 days in England, then use Tell Us Once to inform government services."}, {"id": "eol-2-3", "text": "Look after yourself", "note": "Cruse Bereavement Support: 0808 808 1677. You can ask for your own carer's assessment too."}]}]},
    heart: {"name": "Heart failure", "title": "Living with heart failure", "lede": "Your first 30 days after a heart failure diagnosis, one step at a time.", "kind": "condition", "groups": [{"title": "Week 1: daily checks", "items": [{"id": "heart-0-0", "text": "Ask for a heart failure nurse", "note": "Ask the GP or hospital team for a referral. They are your main contact between appointments."}, {"id": "heart-0-1", "text": "Save the British Heart Foundation helpline", "note": "0808 802 1234. Advice from cardiac nurses."}, {"id": "heart-0-2", "text": "Ask the nurse what checks to do at home", "note": "Ask what to record, and what changes to tell them about."}, {"id": "heart-0-3", "text": "Ask when to call for help", "note": "Ask the GP or nurse when to call them, NHS 111 or 999, and keep the numbers in one place."}]}, {"title": "Weeks 2 to 3: medicines and activity", "items": [{"id": "heart-1-0", "text": "Keep a list of their medicines", "note": "Take it to every appointment. Ask the pharmacist or GP any questions about it."}, {"id": "heart-1-1", "text": "Ask about cardiac rehabilitation", "note": "Supervised exercise and advice that helps people with heart failure feel better."}, {"id": "heart-1-2", "text": "Ask about diet and drinks", "note": "Ask the heart failure nurse whether there is anything they should change."}, {"id": "heart-1-3", "text": "Book flu, COVID and pneumonia vaccines", "note": "Free on the NHS for older people. Ask the GP or pharmacy."}, {"id": "heart-1-4", "text": "Claim Attendance Allowance or PIP", "note": "Attendance Allowance if over State Pension age, Personal Independence Payment if under. Use the Benefits calculator."}]}, {"title": "Weeks 3 to 4: care and you", "items": [{"id": "heart-2-0", "text": "Ask the council for a needs assessment and a carer's assessment", "note": "Both are free, whatever their savings."}, {"id": "heart-2-1", "text": "Make both Lasting Powers of Attorney", "note": "Property and financial affairs, and health and welfare, while they can make the decision."}, {"id": "heart-2-2", "text": "Check Carer's Allowance and Carer's Credit", "note": "Carer's Credit from 20 hours a week, Carer's Allowance from 35."}, {"id": "heart-2-3", "text": "Tell your employer", "note": "One week of unpaid carer's leave a year, and the right to ask for flexible working, both from day one."}]}]},
    copd: {"name": "COPD and breathing", "title": "COPD and breathing problems", "lede": "Your first 30 days of help with COPD or another long-term breathing condition.", "kind": "condition", "groups": [{"title": "Week 1: understand the plan", "items": [{"id": "copd-0-0", "text": "Ask for a written self-management plan", "note": "It says what to do on bad days, and when to call for help."}, {"id": "copd-0-1", "text": "Save the Asthma + Lung UK helpline", "note": "0300 222 5800. Advice from respiratory nurses."}, {"id": "copd-0-2", "text": "Ask what to do on bad days", "note": "Ask the GP or nurse what the plan is if their breathing gets worse."}, {"id": "copd-0-3", "text": "Check inhaler technique", "note": "Ask the pharmacist or practice nurse to watch them use their inhaler. Many people use them wrongly."}]}, {"title": "Weeks 2 to 3: get stronger", "items": [{"id": "copd-1-0", "text": "Ask for pulmonary rehabilitation", "note": "An NHS exercise and education course that improves breathlessness. Ask the GP for a referral."}, {"id": "copd-1-1", "text": "Get help to stop smoking", "note": "The most important step if they smoke. Ask the GP or pharmacy about free NHS support."}, {"id": "copd-1-2", "text": "Book flu, COVID and pneumonia vaccines", "note": "Free on the NHS for older people. Ask the GP or pharmacy."}, {"id": "copd-1-3", "text": "Ask about home oxygen if it's been suggested", "note": "The specialist team explains whether it's needed and how it's set up safely."}]}, {"title": "Weeks 3 to 4: home, care and you", "items": [{"id": "copd-2-0", "text": "Claim Attendance Allowance or PIP", "note": "Attendance Allowance if over State Pension age, Personal Independence Payment if under. Use the Benefits calculator."}, {"id": "copd-2-1", "text": "Ask the council for a free OT home assessment", "note": "Equipment and small changes under £1,000 should be free in England."}, {"id": "copd-2-2", "text": "Ask the council for a needs assessment and a carer's assessment", "note": "Both are free, whatever their savings."}, {"id": "copd-2-3", "text": "Check Carer's Allowance and Carer's Credit", "note": "Carer's Credit from 20 hours a week, Carer's Allowance from 35."}, {"id": "copd-2-4", "text": "Tell your employer", "note": "One week of unpaid carer's leave a year, and the right to ask for flexible working, both from day one."}]}]},
    cancer: {"name": "Cancer", "title": "Supporting someone with cancer", "lede": "Your first 30 days after a cancer diagnosis, one step at a time.", "kind": "condition", "groups": [{"title": "Week 1: know the team", "items": [{"id": "cancer-0-0", "text": "Get the name of their key worker", "note": "Usually a clinical nurse specialist. Your main contact for questions."}, {"id": "cancer-0-1", "text": "Save the Macmillan Support Line", "note": "0808 808 00 00. Help with treatment, money, work and feelings."}, {"id": "cancer-0-2", "text": "Ask for the treatment plan in writing", "note": "What treatment, where, how often, and what side effects to watch for."}, {"id": "cancer-0-3", "text": "Know who to call if they become unwell during treatment", "note": "Many hospitals have a 24-hour chemotherapy or oncology hotline. Save the number."}]}, {"title": "Weeks 2 to 3: money and travel", "items": [{"id": "cancer-1-0", "text": "Claim Attendance Allowance or PIP", "note": "Attendance Allowance if over State Pension age, Personal Independence Payment if under. Use the Benefits calculator."}, {"id": "cancer-1-1", "text": "Ask about help with travel to hospital", "note": "The Healthcare Travel Costs Scheme refunds fares for people on low incomes. Hospitals may have volunteer drivers."}, {"id": "cancer-1-2", "text": "Ask Macmillan about grants and benefits advice", "note": "Macmillan offers one-off grants and free benefits advice."}, {"id": "cancer-1-3", "text": "Apply for a Blue Badge if walking is hard", "note": "Hospital parking can also be free or reduced. Ask the hospital."}]}, {"title": "Weeks 3 to 4: care and you", "items": [{"id": "cancer-2-0", "text": "Ask the council for a needs assessment and a carer's assessment", "note": "Both are free, whatever their savings."}, {"id": "cancer-2-1", "text": "Make both Lasting Powers of Attorney", "note": "Property and financial affairs, and health and welfare, while they can make the decision."}, {"id": "cancer-2-2", "text": "Check Carer's Allowance and Carer's Credit", "note": "Carer's Credit from 20 hours a week, Carer's Allowance from 35."}, {"id": "cancer-2-3", "text": "Tell your employer", "note": "One week of unpaid carer's leave a year, and the right to ask for flexible working, both from day one."}]}]},
    sight: {"name": "Sight and hearing loss", "title": "Sight and hearing loss", "lede": "Help for failing sight or hearing.", "kind": "condition", "groups": [{"title": "Week 1: get checked", "items": [{"id": "sight-0-0", "text": "Book an eye test", "note": "Free on the NHS for over-60s. Opticians can visit at home if they can't get out."}, {"id": "sight-0-1", "text": "Ask the GP for a hearing check", "note": "NHS hearing aids are free after an assessment."}, {"id": "sight-0-2", "text": "Save the RNIB helpline", "note": "0303 123 9999. Help with sight loss."}, {"id": "sight-0-3", "text": "Save the RNID contact line", "note": "0808 808 0123. Help with hearing loss and tinnitus."}]}, {"title": "Weeks 2 to 3: registration and support", "items": [{"id": "sight-1-0", "text": "Ask about a Certificate of Vision Impairment", "note": "An eye specialist can certify sight loss. They can then register with the council for support."}, {"id": "sight-1-1", "text": "Ask the council's sensory team for an assessment", "note": "They can provide aids such as talking clocks, amplified phones and flashing doorbells."}, {"id": "sight-1-2", "text": "Make the home easier to see in", "note": "Brighter bulbs, contrasting colours on steps and edges, and less clutter."}, {"id": "sight-1-3", "text": "Keep hearing aids working", "note": "Ask the audiology clinic for free batteries and repairs."}]}, {"title": "Weeks 3 to 4: money and you", "items": [{"id": "sight-2-0", "text": "Claim Attendance Allowance or PIP", "note": "Attendance Allowance if over State Pension age, Personal Independence Payment if under. Use the Benefits calculator."}, {"id": "sight-2-1", "text": "Ask about the TV Licence", "note": "People registered blind or severely sight impaired get 50% off."}, {"id": "sight-2-2", "text": "Ask the council for a needs assessment and a carer's assessment", "note": "Both are free, whatever their savings."}, {"id": "sight-2-3", "text": "Check Carer's Allowance and Carer's Credit", "note": "Carer's Credit from 20 hours a week, Carer's Allowance from 35."}]}]},
    continence: {"name": "Incontinence", "title": "Bladder and bowel problems", "lede": "Practical help with incontinence. It's common, and often treatable.", "kind": "condition", "groups": [{"title": "Week 1: see the GP", "items": [{"id": "continence-0-0", "text": "Book a GP appointment", "note": "Incontinence often has a treatable cause, such as an infection, constipation or medicines."}, {"id": "continence-0-1", "text": "Ask for a referral to the NHS continence service", "note": "Specialist nurses assess the problem and suggest treatment."}, {"id": "continence-0-2", "text": "Ask which changes need a quick call", "note": "Ask the GP what changes you should tell them about the same day."}]}, {"title": "Weeks 2 to 3: products and routines", "items": [{"id": "continence-1-0", "text": "Ask about free continence products", "note": "After an assessment, the NHS may supply pads in some areas."}, {"id": "continence-1-1", "text": "Ask about routines that might help", "note": "The continence nurse can suggest what's right for them."}, {"id": "continence-1-2", "text": "Make the toilet easy to reach", "note": "A night light, clear path, raised toilet seat or commode. An OT can help."}, {"id": "continence-1-3", "text": "Get a Radar key", "note": "Opens accessible public toilets across the UK. Disability charities and some councils sell them."}]}, {"title": "Weeks 3 to 4: dignity and you", "items": [{"id": "continence-2-0", "text": "Ask how to care for their skin", "note": "Ask the nurse or pharmacist what to use, and about any soreness."}, {"id": "continence-2-1", "text": "Talk about it kindly", "note": "Use their words, keep it private, and focus on comfort, not blame."}, {"id": "continence-2-2", "text": "Claim Attendance Allowance or PIP", "note": "Attendance Allowance if over State Pension age, Personal Independence Payment if under. Use the Benefits calculator."}, {"id": "continence-2-3", "text": "Ask the council for a needs assessment and a carer's assessment", "note": "Both are free, whatever their savings."}, {"id": "continence-2-4", "text": "Check Carer's Allowance and Carer's Credit", "note": "Carer's Credit from 20 hours a week, Carer's Allowance from 35."}]}]},
    diabetes: {"name": "Diabetes", "title": "Diabetes in older age", "lede": "Help with diabetes as needs change in later life.", "kind": "condition", "groups": [{"title": "Week 1: understand the plan", "items": [{"id": "diabetes-0-0", "text": "Ask for the diabetes care plan", "note": "What medicines, what targets, and what to do if they feel unwell."}, {"id": "diabetes-0-1", "text": "Save the Diabetes UK helpline", "note": "0345 123 2399. Advice from trained counsellors."}, {"id": "diabetes-0-2", "text": "Ask about hypos", "note": "Ask the diabetes nurse what a hypo looks like for them and what you should do."}, {"id": "diabetes-0-3", "text": "Ask about sick day rules", "note": "Some diabetes medicines need changing when someone is ill. Ask the GP or nurse."}]}, {"title": "Weeks 2 to 3: regular checks", "items": [{"id": "diabetes-1-0", "text": "Book the yearly diabetes review", "note": "Blood tests, blood pressure, kidney check and a medicines review."}, {"id": "diabetes-1-1", "text": "Ask about foot checks", "note": "Ask the nurse what to look out for, and make sure they have their yearly foot check."}, {"id": "diabetes-1-2", "text": "Go to diabetic eye screening", "note": "Free every year or two. It finds damage before sight is affected."}, {"id": "diabetes-1-3", "text": "Book flu, COVID and pneumonia vaccines", "note": "Free on the NHS for older people. Ask the GP or pharmacy."}]}, {"title": "Weeks 3 to 4: care and you", "items": [{"id": "diabetes-2-0", "text": "Ask if their care plan still fits", "note": "Needs change with age. Ask at the yearly review whether anything should change."}, {"id": "diabetes-2-1", "text": "Claim Attendance Allowance or PIP", "note": "Attendance Allowance if over State Pension age, Personal Independence Payment if under. Use the Benefits calculator."}, {"id": "diabetes-2-2", "text": "Ask the council for a needs assessment and a carer's assessment", "note": "Both are free, whatever their savings."}, {"id": "diabetes-2-3", "text": "Check Carer's Allowance and Carer's Credit", "note": "Carer's Credit from 20 hours a week, Carer's Allowance from 35."}]}]},
    afterfall: {"name": "After a fall or hospital stay", "title": "After a fall or hospital stay", "lede": "Getting back on their feet safely, and stopping it happening again.", "kind": "situation", "groups": [{"title": "Week 1: recovering at home", "items": [{"id": "afterfall-0-0", "text": "Ask about reablement", "note": "Free short-term support at home, usually for up to 6 weeks, to rebuild confidence and skills."}, {"id": "afterfall-0-1", "text": "Ask the GP for a falls check and a medicines review", "note": "Some medicines raise the risk of falls."}, {"id": "afterfall-0-2", "text": "Set up a fall alarm", "note": "See the Fall alarms and home cameras kit."}, {"id": "afterfall-0-3", "text": "Ask the physio what to do after a fall", "note": "Ask them to show you both, so you know the plan."}]}, {"title": "Weeks 2 to 3: get stronger", "items": [{"id": "afterfall-1-0", "text": "Ask for physiotherapy or a strength and balance class", "note": "Strength and balance exercises reduce falls."}, {"id": "afterfall-1-1", "text": "Ask the council for a free OT home assessment", "note": "Equipment and small changes under £1,000 should be free in England."}, {"id": "afterfall-1-2", "text": "Book an eye test", "note": "Free on the NHS for over-60s."}, {"id": "afterfall-1-3", "text": "Check feet and footwear", "note": "Well-fitting shoes with a good grip."}]}, {"title": "Weeks 3 to 4: care and you", "items": [{"id": "afterfall-2-0", "text": "Ask the council for a needs assessment and a carer's assessment", "note": "Both are free, whatever their savings."}, {"id": "afterfall-2-1", "text": "Claim Attendance Allowance or PIP", "note": "Attendance Allowance if over State Pension age, Personal Independence Payment if under. Use the Benefits calculator."}, {"id": "afterfall-2-2", "text": "Check Carer's Allowance and Carer's Credit", "note": "Carer's Credit from 20 hours a week, Carer's Allowance from 35."}, {"id": "afterfall-2-3", "text": "Tell your employer", "note": "One week of unpaid carer's leave a year, and the right to ask for flexible working, both from day one."}]}]},
    delirium: {"name": "Sudden confusion (delirium)", "title": "Sudden confusion (delirium)", "lede": "Confusion that starts over hours or days needs urgent medical help. It is often treatable.", "kind": "situation", "groups": [{"title": "Right now", "items": [{"id": "delirium-0-0", "text": "Get medical help the same day", "note": "Call the GP urgently or NHS 111. If you think it's an emergency, call 999."}, {"id": "delirium-0-1", "text": "Tell the doctor what's normal for them", "note": "Say how they were a few days ago, so the doctor can see what has changed."}, {"id": "delirium-0-2", "text": "Tell them about any recent changes", "note": "New medicines, a recent fall, or anything else that's different."}]}, {"title": "While they recover", "items": [{"id": "delirium-1-0", "text": "Ask the staff how you can help", "note": "Ask the GP, nurse or ward what you can do while they recover."}, {"id": "delirium-1-1", "text": "Bring their glasses and hearing aids", "note": "And familiar things from home, if they're in hospital."}, {"id": "delirium-1-2", "text": "Stay with them if you can", "note": "A familiar face is calming. In hospital, ask about open visiting for carers."}, {"id": "delirium-1-3", "text": "Share a This is me form in hospital", "note": "From Alzheimer's Society: tells staff about their routine, likes and how to calm them."}]}, {"title": "Afterwards", "items": [{"id": "delirium-2-0", "text": "Ask what to expect", "note": "Ask the doctor how recovery is likely to go."}, {"id": "delirium-2-1", "text": "Ask the GP for a follow-up", "note": "Ask whether any further checks are needed once they've recovered."}, {"id": "delirium-2-2", "text": "Ask what to do if it happens again", "note": "Ask the GP, and write the plan down."}]}]}
  },

  // One article a month: one health issue, and how a carer can cope with it.
  articles: [
    { id: "diabetes-christmas", from: "2026-12-01", month: "December 2026", topic: "Diabetes", plan: "diabetes",
      title: "Caring for someone with diabetes over Christmas: how to cope",
      intro: "The festive season can be busy and unsettled, which can make caring harder. This article is about you, the carer: staying organised, sharing the load and looking after yourself. For anything about their health, food or medicines, speak to their GP, diabetes nurse or pharmacist.",
      sections: [
        { h: "Plan the season ahead", p: ["Christmas changes routines: visitors, travel, different mealtimes and services that close for the holidays. Writing down what's happening each day helps everyone know who's doing what."],
          list: ["Put family visits, and who's helping when, in a shared calendar.", "Check when the GP surgery and pharmacy are closed over the holidays.", "Order repeat prescriptions in good time.", "Keep the diabetes team's contact details somewhere easy to find."] },
        { h: "Share the load", p: ["Caring through the holidays shouldn't fall on one person. Agree who covers which days, including lifts to appointments and collecting prescriptions. Kinav's calendar and reminders can help everyone keep track."] },
        { h: "Ask before routines change", p: ["If you're unsure how changes in routine, food or activity over Christmas might affect them, ask their GP, diabetes nurse or pharmacist before the holidays. Writing your questions down first helps, and Kinav's Questions to ask can get you started."] },
        { h: "Know who to call", list: ["For urgent advice, call NHS 111 or use 111.nhs.uk.", "In an emergency, call 999.", "Diabetes UK offers information and support for families."] },
        { h: "Look after yourself", p: ["It's normal to feel stretched at this time of year. Short breaks matter: ask family or friends to take over for an afternoon, and ask the council for a carer's assessment if you haven't had one."] }
      ],
      sources: [
        { name: "Diabetes UK", url: "https://www.diabetes.org.uk/" },
        { name: "NHS 111 online", url: "https://111.nhs.uk/" },
        { name: "NHS: carer's assessments", url: "https://www.nhs.uk/social-care-and-support/support-and-benefits-for-carers/carer-assessments/" }
      ] },
    { id: "copd-winter", month: "November 2026", topic: "COPD and breathing", plan: "copd",
      title: "Caring for someone with COPD this winter: how to cope",
      intro: "Winter can be the hardest time for families living with COPD. This article is about you, the carer: how to stay organised, share the load and look after yourself. For anything about their health, speak to their GP, respiratory nurse, pharmacist or NHS 111. World COPD Day is on 18 November.",
      sections: [
        { h: "Feeling anxious is normal", p: ["Living with someone's breathlessness can leave you on alert all the time, listening out at night and worrying when you're apart. That is very common, and it isn't a sign you're coping badly.", "Naming the worry helps. Many carers find it easier once they know who to call and what the plan is."] },
        { h: "Know who to call", list: [
          "Ask their GP or respiratory nurse whether they have a written plan for bad days, and ask for a copy for you.",
          "Ask the professionals to explain, in their words, when to call them, when to call NHS 111 and when to call 999. Write it down.",
          "Keep the GP, respiratory team, NHS 111 and pharmacy numbers by the phone and in your own phone.",
          "Make sure family members have the same list."
        ]},
        { h: "Questions to take to the next appointment", list: [
          "What should we expect this winter?",
          "What changes should we tell you about, and how quickly?",
          "Is there anything I can learn to help, and who could teach me?",
          "Are they eligible for pulmonary rehabilitation, and can I come too?",
          "Who do we contact out of hours?"
        ]},
        { h: "Share the load", list: [
          "Set up a shared family calendar for appointments, so you're not the only one keeping track. See the Appointments screen.",
          "Agree a simple rota with family or friends for visits, shopping and lifts.",
          "Ask the council for a needs assessment for them, and a carer's assessment for you. Both are free.",
          "Ask about respite, so you can have regular breaks."
        ]},
        { h: "Look after yourself", p: ["Keep up your own appointments, sleep and time away. Ask your GP whether you can get a free flu vaccine as a carer.", "Talk to someone. The Asthma + Lung UK helpline is 0300 222 5800 for questions about living with lung conditions. Samaritans are on 116 123, any time, if it all feels too much."] }
      ],
      sources: [
        { name: "Asthma + Lung UK: contact the helpline", url: "https://www.asthmaandlung.org.uk/about-us/contact-us" },
        { name: "NHS: carer's assessments", url: "https://www.nhs.uk/social-care-and-support/support-and-benefits-for-carers/carer-assessments/" }
      ]
    }
  ],

  kits: [
    { id: "home-choice", group: "Arranging care", name: "Choosing a nursing home", what: "Shortlist, visit and ask the right questions.", steps: [
      { t: "Ask the council for a free needs assessment", d: "It confirms what level of care is needed. Anyone can ask, whatever their savings." },
      { t: "Work out how it will be paid for", d: "Use the Care costs tool. If savings are above £23,250 they will usually pay their own fees at first. Ask the council for a financial assessment either way." },
      { t: "Shortlist 3 to 5 homes", d: "Use Find care, filter to nursing homes and dementia care if needed, and read each home's latest CQC report." },
      { t: "Phone each home", d: "Say: \"I'm looking for a nursing place for my mum. Do you have a vacancy, what is the weekly fee, and what does it include?\" Ask whether they keep residents if their savings run out and the council starts paying." },
      { t: "Visit at least twice", d: "Go once at a mealtime. Look for staff talking with residents, call bells answered quickly, residents doing things, and a clean, fresh home." },
      { t: "Ask the manager", d: "How many nurses are on each shift? How much do you use agency staff? How do you support someone who becomes distressed? How often does a GP visit? Can residents stay here to the end of their life?" },
      { t: "Ask about NHS help with nursing costs", d: "The NHS may pay a contribution towards nursing care. Ask about an NHS Continuing Healthcare check too." },
      { t: "Read the contract before signing", d: "Use the Before you sign kit." },
      { t: "Plan the move", d: "Bring familiar things and photos, label clothes, and tell the GP, pharmacy, bank and pension providers about the new address." }
    ]},
    { id: "home-care", group: "Arranging care", name: "Setting up care at home", what: "Compare agencies and agree a care plan.", steps: [
      { t: "Ask the council for a free needs assessment", d: "Ask about reablement too: free short-term support at home, usually for up to 6 weeks." },
      { t: "List what help is needed", d: "Write down the times of day and tasks, for example getting up and washed, lunch and medication, help to bed." },
      { t: "Find 3 agencies", d: "Use Find care with \"Care at home\", and read each agency's latest CQC report." },
      { t: "Call each agency", d: "Ask: What is your hourly rate, and is it higher at weekends? What is the shortest visit? Will Mum see the same carers? Are your carers trained in dementia care? What happens if a carer is late or can't come? How much notice do I give to stop?" },
      { t: "Get it in writing", d: "Ask for the rates, terms and notice period by email before you agree." },
      { t: "Agree a written care plan", d: "The agency should visit first and write down what carers will do at each visit." },
      { t: "Be there for the first visits", d: "Leave a notebook at home for carers and family to write in." },
      { t: "Review after a month", d: "Ask the council for a review if needs change." }
    ]},
    { id: "live-in", group: "Arranging care", name: "Arranging live-in care", what: "Find, check and plan cover for a live-in carer.", steps: [
      { t: "Choose the type of service", d: "A managed service employs the carer and must be registered with CQC. An introductory agency only introduces carers, so you take on more responsibility." },
      { t: "Check the space", d: "A live-in carer needs their own bedroom." },
      { t: "Compare the cost", d: "Ask for the weekly fee and put it into the Care costs tool to see how long savings last." },
      { t: "Meet the carer before they start", d: "Ask the agency how they match carers, and what happens if it isn't working." },
      { t: "Plan breaks and holidays", d: "Ask who covers the carer's daily breaks, days off and holidays." },
      { t: "Tell the home insurer", d: "Let them know someone else will be living in the home." },
      { t: "Review after the first month", d: "Check the care plan still fits." }
    ]},
    { id: "safety", group: "Hospital and safety", name: "Home safety and grants", what: "Free OT assessment, free equipment and grants.", steps: [
      { t: "Ask for a free OT home assessment", d: "Call the council's adult social care team and ask for an occupational therapist to assess the home." },
      { t: "Ask what equipment is free", d: "In England, councils should provide equipment and small adaptations costing under £1,000 free of charge." },
      { t: "Ask about a Disabled Facilities Grant", d: "Up to £30,000 in England for bigger changes such as a stairlift or level-access shower. It is means-tested." },
      { t: "Book a free fire safety visit", d: "Your local fire and rescue service checks smoke alarms and fire risks." },
      { t: "Consider a fall alarm", d: "Ask the council about telecare, such as a pendant alarm or fall detector. See the Fall alarms and home cameras kit." },
      { t: "Use trusted traders", d: "Ask the council about its trusted trader scheme, and get 2 or 3 written quotes." }
    ]},
    { id: "alarms", group: "Hospital and safety", name: "Fall alarms and home cameras", what: "Get help quickly after a fall, and use cameras with care.", steps: [
      { t: "Ask the council about a personal alarm", d: "Most councils run a telecare or lifeline service: a button worn on the wrist or neck that calls a 24-hour team. Ask during the needs assessment or OT visit. There is usually a weekly charge." },
      { t: "Choose the right type of alarm", d: "A button they press; an automatic fall detector that calls for help even if they can't press it; a GPS alarm if they go out alone; or a smartwatch with fall detection. If they might forget to press a button, choose automatic fall detection." },
      { t: "Pick who responds", d: "Give the alarm service 2 or 3 people who live nearby and can get there quickly. Some services offer their own responders if family is far away." },
      { t: "Fit a key safe", d: "A key safe by the front door lets responders and ambulance crews get in without breaking the door. Choose a police-approved model." },
      { t: "Make sure it's worn", d: "Most fall alarms are waterproof, so they can be worn in the shower, where many falls happen. Test it once a month." },
      { t: "Consider sensors instead of cameras", d: "Bed, chair and door sensors, or activity sensors that learn their routine, can alert you to a fall or a night-time wander without filming them." },
      { t: "If you want cameras, talk to them first", d: "If they can make the decision, they must agree. If they can't, any camera must be in their best interests and the least intrusive option. Involve family and anyone with a health and welfare Power of Attorney." },
      { t: "Keep cameras out of private rooms", d: "Don't put cameras in bedrooms or bathrooms. Avoid recording sound unless there's a clear reason, as it's more intrusive." },
      { t: "Tell carers about any cameras", d: "Let care workers and the agency know where cameras are and why. Recording people without telling them damages trust." },
      { t: "Keep the cameras private and secure", d: "Change the default password and turn on two-step login. If a camera films beyond their property, such as the street or a neighbour's garden, data protection law applies, so point cameras inside the home." }
    ]},
    { id: "hospital", group: "Hospital and safety", name: "Leaving hospital", what: "Make sure the right help is in place at home.", steps: [
      { t: "Ask who is planning the discharge", d: "Ask the ward for the name of the person coordinating it, and for the discharge plan." },
      { t: "Be clear about what you can do", d: "If you can't provide care, say so. Don't let the plan assume family will cover." },
      { t: "Ask about free short-term care", d: "Ask about reablement or intermediate care to help them recover at home." },
      { t: "Ask about NHS Continuing Healthcare", d: "If health needs are complex, ask for the Continuing Healthcare checklist before discharge." },
      { t: "Get equipment in place", d: "Make sure equipment such as a commode or raised toilet seat is delivered before they come home." },
      { t: "Sort out medicines", d: "Ask for a list of medicines, who will collect them, and whether the pharmacy can provide blister packs." },
      { t: "Check the follow-up", d: "Make sure the GP has the discharge letter, and ask whether a district nurse will visit." }
    ]},
    { id: "blue-badge", group: "Money, rights and forms", name: "Applying for a Blue Badge", what: "Parking closer to where they need to go. England's rules.", steps: [
      { t: "Check if they qualify automatically", d: "They do if they get the higher rate mobility part of DLA; PIP with 8 points or more for \"moving around\"; PIP with 10 points for descriptor E under \"planning and following journeys\"; are registered blind (severely sight impaired); or get War Pensioners' Mobility Supplement or certain Armed Forces compensation. Attendance Allowance on its own doesn't count." },
      { t: "If not, they may still qualify", d: "The council decides. For example, if walking is very difficult because of pain, breathlessness or the time it takes, or isn't safe for them. Non-visible conditions can count too, such as being a serious risk near traffic, struggling severely to plan or follow a journey, or becoming extremely anxious in public places." },
      { t: "Gather the documents", d: "A recent head-and-shoulders digital photo. A photo or scan of proof of identity (birth certificate, passport or driving licence) and proof of address (Council Tax bill or a recent government letter). Their National Insurance number, any benefit award letter (for PIP, the scores), and the current badge details if renewing." },
      { t: "Write down how getting about affects them", d: "The form asks how far they can walk and how long it takes, what help they need, and who is involved in their care. A note of a typical trip, such as to the shops or the GP, makes this easier." },
      { t: "Apply online", d: "Use GOV.UK: gov.uk/apply-blue-badge. You can apply on their behalf, and save and come back later. Or ask the council for a paper form." },
      { t: "Pay the fee", d: "Up to £10 in England. The council tells you how to pay." },
      { t: "Wait for the decision", d: "Usually within 12 weeks. The council may ask for more information or invite them to a mobility assessment." },
      { t: "If it's refused", d: "Ask the council to reconsider, explaining anything they missed. You can reapply if things change. Citizens Advice (CAB) can help: Adviceline (England) 0800 144 8848." },
      { t: "Use it the right way", d: "The badge is theirs: use it only when they're travelling in the car, as driver or passenger. Show it on the dashboard, with the clock where needed. Misuse can mean a fine of up to £1,000." },
      { t: "Set a renewal reminder", d: "Badges usually last up to 3 years, and you must reapply before it runs out. In Calendar, choose Reminder, then Blue Badge renewal, and it will remind you 12 weeks before." }
    ]},
    { id: "contract", group: "Money, rights and forms", name: "Before you sign a care home contract", what: "Fees, increases, top-ups and notice.", steps: [
      { t: "Get the contract in advance", d: "Ask for it before moving day, and take time to read it." },
      { t: "Check the fees", d: "What is the weekly fee, and what costs extra, such as hairdressing, trips or toiletries?" },
      { t: "Check how fees go up", d: "How often do fees rise, by how much, and how much notice do they give?" },
      { t: "Ask about top-up fees", d: "If the council starts paying later, will someone need to pay a top-up? Who agrees to it?" },
      { t: "Check deposits and payment in advance", d: "How much, and when is it returned?" },
      { t: "Check notice terms", d: "How much notice is needed to leave, and how many days of fees are charged after a death?" },
      { t: "Check when a resident can be asked to leave", d: "Ask what the reasons are and what notice they give." },
      { t: "Know how to complain", d: "Ask for the complaints process. If it isn't resolved, you can go to the Local Government and Social Care Ombudsman." },
      { t: "Get free help if anything is unclear", d: "Citizens Advice (CAB) can explain your rights on fees, notice and unfair terms. Call the Citizens Advice consumer helpline on 0808 223 1133, or the Adviceline (England) on 0800 144 8848." }
    ]}
  ],

  // Calendar reminders: weeks = how long before the due date to remind; repeat = "", "yearly" or "monthly"
  reminders: [
    { id: "blue-badge", label: "Blue Badge renewal", due: "Date the badge expires", weeks: 12, repeat: "",
      title: "Renew the Blue Badge", details: "The Blue Badge expires soon. Reapply before it runs out at gov.uk/apply-blue-badge. Have a recent photo, proof of identity and address, and any benefit award letter ready." },
    { id: "aa-review", label: "Attendance Allowance or PIP review", due: "Award end or review date (on the award letter)", weeks: 8, repeat: "",
      title: "Attendance Allowance or PIP review coming up", details: "Look out for the review form from the Department for Work and Pensions and send it back by the date given. Citizens Advice (0800 144 8848) can help with the form." },
    { id: "claim-chase", label: "Chase a benefit claim", due: "Date to chase if there's no decision", weeks: 0, repeat: "",
      title: "Chase the benefit claim", details: "If there's no decision yet, call the benefit's helpline with the claim reference and National Insurance number. Note who you spoke to and what they said." },
    { id: "council-charges", label: "Council financial reassessment", due: "Date of the yearly reassessment", weeks: 4, repeat: "yearly",
      title: "Council care charges reassessment", details: "The council reviews care charges each year. Gather bank statements, pension and benefit letters. Ask for the result in writing." },
    { id: "care-review", label: "Care plan or needs review", due: "Date the review is due", weeks: 2, repeat: "yearly",
      title: "Care plan review due", details: "The council should review the care and support plan at least once a year, or sooner if needs change. Note what's working and what isn't, and ask for the review if it hasn't been booked." },
    { id: "carer-assessment", label: "Carer's assessment review", due: "Date of your last carer's assessment", weeks: 0, repeat: "yearly",
      title: "Ask for a carer's assessment review", details: "Ask the council to review your carer's assessment, especially if caring has become harder or your work has changed. It's free." },
    { id: "fee-rise", label: "Care fee increase", due: "Date the new fee starts", weeks: 6, repeat: "yearly",
      title: "Care fees are going up", details: "Check the new weekly fee against the contract, and whether savings still cover it. If the council pays part, ask whether a top-up will change. Citizens Advice consumer helpline: 0808 223 1133." },
    { id: "council-tax", label: "Council tax discount check", due: "Date the new council tax bill arrives (usually March)", weeks: 0, repeat: "yearly",
      title: "Check the council tax discount", details: "Check the new bill still shows any discount, disregard or exemption, such as for severe mental impairment or for a carer. Call the council if it's missing." },
    { id: "lpa", label: "Lasting Power of Attorney follow-up", due: "Date to check on the registration", weeks: 0, repeat: "",
      title: "Check the Lasting Power of Attorney registration", details: "If you haven't heard from the Office of the Public Guardian, contact them with the reference number to check progress." },
    { id: "alarm-test", label: "Test the fall alarm and smoke alarms", due: "First test date", weeks: 0, repeat: "monthly",
      title: "Test the alarms", details: "Press the fall alarm pendant's test button, or call the alarm company to test it. Press the test button on smoke and carbon monoxide alarms. Replace batteries if needed." },
    { id: "other", label: "Something else", due: "Date it's due", weeks: 0, repeat: "",
      title: "", details: "" }
  ],

  // Two questions per plan, added to appointments automatically. Who to ask and what happens next, never health advice.
  planQuestions: {
    dementia: ["Can we be referred to an Admiral Nurse or dementia adviser?", "Who should we contact if memory or behaviour changes?"],
    parkinsons: ["Can we be referred to a Parkinson's nurse?", "When is the next medicines review?"],
    mobility: ["Can we have an occupational therapy or physiotherapy assessment?", "Can we be referred to the local falls service?"],
    stroke: ["What rehabilitation is available at home?", "Can we be referred to the Stroke Association's support service?"],
    eol: ["Can we be referred to the palliative care team or local hospice?", "Who do we call out of hours?"],
    heart: ["Can we be referred to a heart failure nurse?", "Who do we call if things change?"],
    copd: ["Can we be referred to pulmonary rehabilitation?", "Is there a respiratory nurse we can contact?"],
    cancer: ["Who is our clinical nurse specialist?", "What support is there for family, such as Macmillan?"],
    sight: ["Can we be referred to the council's sensory support team?", "When is the next sight or hearing test due?"],
    continence: ["Can we be referred to the NHS continence service?", "Are pads or other products available on the NHS?"],
    diabetes: ["Who is our diabetes contact?", "When are the next checks due?"],
    afterfall: ["Can we be referred to the falls service?", "Is reablement available at home?"],
    delirium: ["What happens next, and what should we watch for?", "Who do we contact if it happens again?"]
  },

  // Question lists: people pick the ones they want, then write answers beside them
  // Free version: five key questions per topic. The detailed lists are planned for Kinav Pro.
  questions: [
    { id: "carehome", name: "Visiting a care home", items: [
      "Do you have a vacancy, and when?",
      "What is the weekly fee, and what costs extra?",
      "How often do fees go up, and by how much?",
      "Will you accept the council's rate if savings run out? Would a top-up be needed?",
      "How many staff are on duty in the day and at night?"
    ]},
    { id: "homecare", name: "Choosing a home care agency", items: [
      "What is your hourly rate? Is it higher at evenings and weekends?",
      "What is the shortest visit you do?",
      "Will the same carers come each time?",
      "What happens if a carer is late or can't come?",
      "What training do your carers have, for example in dementia care or moving and handling?"
    ]},
    { id: "assessment", name: "Council needs assessment", items: [
      "When will the assessment happen, and who will do it?",
      "Can I be there?",
      "Can I have a carer's assessment too?",
      "What support could be offered?",
      "Could they have reablement first?"
    ]},
    { id: "discharge", name: "Leaving hospital", items: [
      "When is the planned discharge date?",
      "What support will be in place at home, and from when?",
      "Is reablement or intermediate care available?",
      "Will any equipment be delivered before they come home?",
      "Should they be assessed for NHS continuing healthcare?"
    ]},
    { id: "appointment", name: "GP or hospital appointment", items: [
      "What happens next?",
      "Who is our main contact, and how do we reach them?",
      "When is the next review?",
      "What should we do if things change?",
      "Can we have a copy of any letters?"
    ]}
  ],

  benefits: {
    questions: [
      { id: "age", q: "Is the person you care for over State Pension age?", options: ["Yes", "No"] },
      { id: "help", q: "Have they needed help with personal care or supervision for 6 months or more?", options: ["Yes", "Not yet", "No"] },
      { id: "alone", q: "Do they live alone?", options: ["Yes", "No"] },
      { id: "income", q: "Is their income mainly the State Pension?", options: ["Yes", "No", "Not sure"] },
      { id: "hours", q: "How many hours a week do you spend caring?", options: ["Under 20", "20 to 34", "35 or more"] },
      { id: "earn", q: "Do you earn more than £204 a week after tax and expenses?", options: ["Yes", "No"] }
    ]
  },

  // Weekly fees and hourly home care rates. Areas without a published figure borrow Surrey's.
  areas: {
    london: { name: "London", res: 1598, nurs: 1680, hourly: 34.42, note: "London average from the Lottie care index (2026)." },
    surrey: { name: "Surrey", res: 1501, nurs: 1647, hourly: 34.42, note: "Surrey County Council averages for self-funders." },
    herts: { name: "Hertfordshire", res: 1501, nurs: 1647, hourly: 34.42, note: "No local figure yet, so Surrey averages are used. Enter a local quote." },
    kent: { name: "Kent", res: 1501, nurs: 1647, hourly: 34.42, note: "No local figure yet, so Surrey averages are used. Enter a local quote." },
    mk: { name: "Milton Keynes", res: 1501, nurs: 1647, hourly: 34.42, note: "No local figure yet, so Surrey averages are used. Enter a local quote." },
    other: { name: "Elsewhere in England", res: 1501, nurs: 1647, hourly: 34.42, note: "No local figure yet, so Surrey averages are used. Enter a local quote." }
  }
};
